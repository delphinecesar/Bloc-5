# Bloc 5: Getaround Analysis

## Links
- Streamlit dashboard: https://getaround-dashboard-dc-86e9a13809ab.herokuapp.com
- API: https://getaround-api-dc-e2058e383f63.herokuapp.com/docs

## Project 🚧

For this case study, we suggest that you put yourselves in our shoes, and run an analysis we made back in 2017 🔮 🪄

When using Getaround, drivers book cars for a specific time period, from an hour to a few days long. They are supposed to bring back the car on time, but it happens from time to time that drivers are late for the checkout.

Late returns at checkout can generate high friction for the next driver if the car was supposed to be rented again on the same day : Customer service often reports users unsatisfied because they had to wait for the car to come back from the previous rental or users that even had to cancel their rental because the car wasn’t returned on time.

## Goals 🎯

In order to mitigate those issues we’ve decided to implement a minimum delay between two rentals. A car won’t be displayed in the search results if the requested checkin or checkout times are too close from an already booked rental.

It solves the late checkout issue but also potentially hurts Getaround/owners revenues: we need to find the right trade off.

Our Product Manager still needs to decide:

threshold: how long should the minimum delay be? </br>
scope: should we enable the feature for all cars?, only Connect cars? </br>
In order to help them make the right decision, they are asking you for some data insights. Here are the first analyses they could think of, to kickstart the discussion. Don’t hesitate to perform additional analysis that you find relevant.

Which share of our owner’s revenue would potentially be affected by the feature? </br>
How many rentals would be affected by the feature depending on the threshold and scope we choose? </br>
How often are drivers late for the next check-in? How does it impact the next driver? </br>
How many problematic cases will it solve depending on the chosen threshold and scope? </br>

## Certification information
* Email adress: delphinecesar@gmail.com
* Video presentation:
