import pandas as pd
import re
import json
from scipy.stats import poisson
import torch
import torch.nn as nn
import pandas as pd
from joblib import load
import numpy as np
import warnings

warnings.filterwarnings('ignore')

# big_df = pd.read_excel('/content/1900-2024_public_emdat_custom_request_2024-04-20_39efc9b7-44de-48fc-8353-bf01f2e06539.xlsx')
big_df = pd.read_excel('backend/2000-2024_public_emdat_custom_request_2024-04-21_e453b16f-3ab1-447c-8b91-47a2a3f9f355.xlsx')

df = big_df[["Disaster Group","Disaster Subgroup", "Disaster Subtype", "Location", "Start Year", "Total Deaths", "No. Injured", "Total Damage, Adjusted ('000 US$)"]].copy()
df['Location'] = df['Location'].astype(str)

# Define state names and their abbreviations
states = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

# Combine into a search pattern
state_pattern = re.compile(r'\b(' + '|'.join(re.escape(state) for state in states.keys()) + r'|\b' + '|'.join(re.escape(states[state]) for state in states) + r')\b', re.IGNORECASE)

# Function to extract states
def extract_states(location):
    matches = state_pattern.findall(location)
    unique_states = set(matches)  # Use set to remove duplicates
    # Convert abbreviations to full state names for uniformity
    full_names = {abbrev: name for name, abbrev in states.items()}
    final_states = {full_names.get(state.upper(), state.title()) for state in unique_states}
    return ', '.join(sorted(final_states))

df['Location'] = df['Location'].apply(extract_states)
df = df[df['Location'] != '']
df = df.fillna(0)
df['Location'] = df['Location'].str.split(',')

# Calculate the number of locations in each row to divide quantitative values
df['Location_Count'] = df['Location'].apply(len)

# Explode the 'Location' column
expanded_df = df.explode('Location')

# Adjust the quantitative values by dividing by the number of locations
expanded_df['Total Deaths'] = round(expanded_df['Total Deaths'] / expanded_df['Location_Count'])
expanded_df['No. Injured'] = round(expanded_df['No. Injured'] / expanded_df['Location_Count'])
expanded_df["Total Damage, Adjusted ('000 US$)"] = round(expanded_df["Total Damage, Adjusted ('000 US$)"] / expanded_df['Location_Count'])
expanded_df.drop('Location_Count', axis=1, inplace=True)

# Mapping dictionary for disaster subtypes
subtype_mapping = {
    'Flood (General)': 'Flood', 
    'Coastal flood': 'Flood',
    'Flash flood' : 'Flood',
    'Riverine flood' : 'Flood',
    
    'Blizzard/Winter storm': 'Severe Storm', 
    'Extra-tropical storm': 'Severe Storm',
    'Storm (General)': 'Severe Storm',
    'Lightning/Thunderstorms': 'Severe Storm',
    
    'Forest fire': 'Wildfire', 
    'Land fire (Brush, Bush, Pasture)': 'Wildfire',
    'Wildfire (General)': 'Wildfire',
    
    'Ground movement': 'Earthquake', 
    
    'Landslide (wet)': 'Landslide', 
    'Mudslide': 'Landslide', 
    
    'Tornado': 'Tornado', 
    'Tropical cyclone': 'Cyclone',
    'Severe weather': 'Severe Weather',
}

# Replace the disaster subtypes with the new generalized categories
expanded_df['Disaster Subtype'] = expanded_df['Disaster Subtype'].replace(subtype_mapping)

# Definition of the Autoencoder class
class Autoencoder(nn.Module):
    def __init__(self, num_features):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(num_features, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 16),  # Encoded representation
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, num_features),  # Output size same as input size
            nn.Sigmoid()  # Use sigmoid if the input is normalized between 0 and 1
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return encoded, decoded

# Definition of the RegressionNet class
class RegressionNet(nn.Module):
    def __init__(self):
        super(RegressionNet, self).__init__()
        self.fc1 = nn.Linear(16, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, 1)  # Predicting a single value

    def forward(self, x):
        x = self.relu(self.fc1(x))
        return self.fc2(x)

# Function to load models
def load_models():
    num_features = 59  # Adjust this to match the original model's feature size
    autoencoder = Autoencoder(num_features)
    regression_model = RegressionNet()

    autoencoder.load_state_dict(torch.load('backend/autoencoder_weights.pth'))
    regression_model.load_state_dict(torch.load('backend/regression_model_weights.pth'))
    return autoencoder, regression_model

# Function to predict damage
def predict_damage(input_data):
    autoencoder, regression_model = load_models()
    preprocessor = load('backend/preprocessor.joblib')

    df = pd.DataFrame([input_data])
    X = preprocessor.transform(df).toarray()  # Using the same preprocessor as during training
    X_tensor = torch.tensor(X.astype(np.float32))  # Convert to tensor

    autoencoder.eval()
    regression_model.eval()
    with torch.no_grad():
        encoded_features, _ = autoencoder(X_tensor)
        predicted_damage = regression_model(encoded_features)

    if predicted_damage.item() < 0:
        return int(-predicted_damage.item() * 1e7)
    return int(predicted_damage.item() * 1e7)

expanded_df['Location'] = expanded_df['Location'].str.strip()
# Use Poisson distribution to estimate the probability of at least one disaster next year at a specific state and estimated damage cost of the disaster
def pred_disaster(Statename):
  
  years_of_data = expanded_df['Start Year'].max() - expanded_df['Start Year'].min()
  State_df = expanded_df[expanded_df['Location'] == Statename]
  Disasters = State_df['Disaster Subtype'].unique()

  prediction_results = {}

  for disaster in Disasters:
    input_features = {
        'Start Year': 2025,
        'Disaster Subtype': disaster,
        'Location': Statename
    }
    predicted_damage = predict_damage(input_features)
    disaster_count = State_df['Disaster Subtype'].value_counts()[disaster]
    prediction = 1 - poisson.pmf(0, disaster_count/years_of_data)
    prediction_results[disaster] = [f"{prediction:.2%}", predicted_damage]

  # Convert results to JSON
  prediction_json = json.dumps(prediction_results, indent=4)
  return prediction_json

# print(pred_disaster('Florida'))
# print("-----------------------------------")
# print(pred_disaster('New Mexico'))