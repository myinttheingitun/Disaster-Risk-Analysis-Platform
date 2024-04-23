# Disaster Risk Analytics Platform

## About the Project

Welcome to our project, "Disaster Risk Analytics Platform," developed with an aim to provide comprehensive disaster risk analysis for investment firms operating within the U.S. markets. Using advanced statistical analysis and deep learning technologies, this platform helps predict potential disasters and their financial impacts on various states, aiding firms in making informed, resilient investment decisions.

## Live Demo

The web application is currently hosted and can be accessed http://imonbera13.pythonanywhere.com/.

## Features

- **Statistical Modeling:** Utilizes Poisson's distribution to accurately model the frequency of disaster events.
- **Deep Learning Integration:** Features an autoencoder for efficient data encoding and a custom deep learning-based regression model ("Regression Net") for financial damage estimation.
- **User-Friendly Interface:** A Flask web application with an intuitive map interface allows users to interact with and visualize risk data effectively.
- **Scalable Deployment:** Hosted on AWS EC2 to ensure scalable and reliable access.

## Built With

- **Flask**: For backend framework.
- **HTML/CSS/JavaScript**: For creating a responsive and interactive front-end.
- **Machine Learning & Deep Learning**: Powers the core analytics of the platform.
- **Autoencoders**: Used for data encoding and dimensionality reduction.
- **RegressionNet**: A custom deep learning model for estimating financial impacts.

## Data Sources

This project utilizes the comprehensive disaster dataset provided by [EM-DAT](https://www.emdat.be/), which was instrumental in developing our predictive models.

## Codefest Participation

This project was developed for the Philly Codefest. More information about the event can be found at [event.phillycodefest.com](https://event.phillycodefest.com/).

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

- Python 3.x
- npm (Node package manager)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/invcble/Disaster-Risk-Analysis-Platform
   ```
