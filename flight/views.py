from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import FlightForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from sklearn.preprocessing import LabelEncoder
# from flightpredict import model
import pandas as pd
import numpy as np
import pickle


# Create your views here.
def flightpredict(request):
    flight_form = FlightForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if flight_form.is_valid():
            # print(request.POST)
            # print(request.POST.get('source'))
            # print(request.POST.get('destination'))
            # print(request.POST.get('departure_date'))
            # print(request.POST.get('arrival_date'))
            # print(request.POST.get('airline'))
            # print(request.POST.get('stoppage'))
            # source=request.POST.get('source')
            # destination=request.POST.get('destination')
            departure_date=request.POST.get('departure_date')
            arrival_date=request.POST.get('arrival_date')
            # airline=request.POST.get('airline')
            # stoppage=request.POST.get('stoppage')
            # return render(request,'flight.html',{'flight':flight_form})
            # Create a view function that takes in the user's input and returns the predicted flight price
    # Get the user's input
            # total_stops = request.POST.get('stoppage')
            # journey_day = int(pd.to_datetime(departure_date, format="%Y-%m-%dT%H:%M").day)
            # journey_month = int(pd.to_datetime(departure_date, format ="%Y-%m-%dT%H:%M").month)
            # dep_hour = int(pd.to_datetime(departure_date, format ="%Y-%m-%dT%H:%M").hour)
            # dep_min =int(pd.to_datetime(departure_date, format ="%Y-%m-%dT%H:%M").minute)
            # arrival_hour = int(pd.to_datetime(arrival_date, format ="%Y-%m-%dT%H:%M").hour)
            # arrival_min = int(pd.to_datetime(arrival_date, format ="%Y-%m-%dT%H:%M").minute)
            # dur_hour = abs(arrival_hour - dep_hour)
            # dur_min = abs(arrival_min - dep_min)
            # airline = request.POST.get('airline')
            # source = request.POST.get('source')
            # destination = request.POST.get('destination')

            # # Predict the flight price
            # prediction = model.predict(
            #     [total_stops, journey_day, journey_month, dep_hour, dep_min, arrival_hour, arrival_min, dur_hour, dur_min, airline, source, destination]
            # )

            # # Round the predicted flight price to two decimal places
            # output = round(prediction[0], 2)

            # # Return the predicted flight price as an HTTP response
            # return HttpResponse(output)

            with open('flight_rf.pkl', 'rb') as f:
                model = pickle.load(f)

            # Extract input features from the request
            # source = request.POST.get('source')
            # destination = request.POST.get('destination')
            # airline = request.POST.get('airline')
            # total_stops = int(request.POST.get('stoppage'))
            # print(departure_date)
            # print(pd.to_datetime(departure_date, format="%Y-%m-%dT%H:%M").day)
            # journey_day = int(pd.to_datetime(departure_date, format="%Y-%m-%dT%H:%M").day)
            # journey_month = int(pd.to_datetime(departure_date, format ="%Y-%m-%dT%H:%M").month)
            # dep_hour = int(pd.to_datetime(departure_date, format ="%Y-%m-%dT%H:%M").hour)
            # dep_min =int(pd.to_datetime(departure_date, format ="%Y-%m-%dT%H:%M").minute)
            # arrival_hour = int(pd.to_datetime(arrival_date, format ="%Y-%m-%dT%H:%M").hour)
            # arrival_min = int(pd.to_datetime(arrival_date, format ="%Y-%m-%dT%H:%M").minute)
            # dur_hour = abs(arrival_hour - dep_hour)
            # dur_min = abs(arrival_min - dep_min)

            # # Create a pandas DataFrame with the input features
            # data = pd.DataFrame({
            #     'Airline': [airline],
            #     'Source': [source],
            #     'Destination': [destination],
            #     'Total_Stops': [total_stops],
            #     'Journey_Day': [journey_day],
            #     'Journey_Month': [journey_month],
            #     'Dep_Hour': [dep_hour],
            #     'Dep_Min': [dep_min],
            #     'Arrival_Hour': [arrival_hour],
            #     'Arrival_Min': [arrival_min],
            #     'Duration_Hours': [dur_hour],
            #     'Duration_Minutes': [dur_min]
            # })

            # # Encode categorical features using LabelEncoder
            # le = LabelEncoder()
            # data['Airline'] = le.fit_transform(data['Airline'])
            # data['Source'] = le.fit_transform(data['Source'])
            # data['Destination'] = le.fit_transform(data['Destination'])

            # # Make the flight price prediction
            # predicted_price = model.predict(data)

            # # Return the predicted price as a JSON response
            # return JsonResponse({'predicted_price': predicted_price[0]})
            date_dep = request.POST.get("departure_date")
            Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
            Journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
            # print("Journey Date : ",Journey_day, Journey_month)

            # Departure
            Dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
            Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
            # print("Departure : ",Dep_hour, Dep_min)

            # Arrival
            date_arr = request.POST.get("arrival_date")
            Arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
            Arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
            # print("Arrival : ", Arrival_hour, Arrival_min)

            # Duration
            dur_hour = abs(Arrival_hour - Dep_hour)
            dur_min = abs(Arrival_min - Dep_min)
            # print("Duration : ", dur_hour, dur_min)

            # Total Stops
            Total_stops = int(request.POST.get("stoppage"))
            # print(Total_stops)

            # Airline
            # AIR ASIA = 0 (not in column)
            airline=request.POST.get("airline")
            if(airline=='Jet Airways'):
                Jet_Airways = 1
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0 

            elif (airline=='IndiGo'):
                Jet_Airways = 0
                IndiGo = 1
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0 

            elif (airline=='Air India'):
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 1
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0 
                
            elif (airline=='Multiple carriers'):
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 1
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0 
                
            elif (airline=='SpiceJet'):
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 1
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0 
                
            elif (airline=='Vistara'):
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 1
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0

            elif (airline=='GoAir'):
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 1
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0

            elif (airline=='Multiple carriers Premium economy'):
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 1
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0

            elif (airline=='Jet Airways Business'):
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 1
                Vistara_Premium_economy = 0
                Trujet = 0

            elif (airline=='Vistara Premium economy'):
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 1
                Trujet = 0
                
            elif (airline=='Trujet'):
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 1

            else:
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0

            # print(Jet_Airways,
            #     IndiGo,
            #     Air_India,
            #     Multiple_carriers,
            #     SpiceJet,
            #     Vistara,
            #     GoAir,
            #     Multiple_carriers_Premium_economy,
            #     Jet_Airways_Business,
            #     Vistara_Premium_economy,
            #     Trujet)

            # Source
            # Banglore = 0 (not in column)
            Source = request.POST.get("source")
            if (Source == 'Delhi'):
                s_Delhi = 1
                s_Kolkata = 0
                s_Mumbai = 0
                s_Chennai = 0

            elif (Source == 'Kolkata'):
                s_Delhi = 0
                s_Kolkata = 1
                s_Mumbai = 0
                s_Chennai = 0

            elif (Source == 'Mumbai'):
                s_Delhi = 0
                s_Kolkata = 0
                s_Mumbai = 1
                s_Chennai = 0

            elif (Source == 'Chennai'):
                s_Delhi = 0
                s_Kolkata = 0
                s_Mumbai = 0
                s_Chennai = 1

            else:
                s_Delhi = 0
                s_Kolkata = 0
                s_Mumbai = 0
                s_Chennai = 0

            # print(s_Delhi,
            #     s_Kolkata,
            #     s_Mumbai,
            #     s_Chennai)

            # Destination
            # Banglore = 0 (not in column)
            Source = request.POST.get("destination")
            if (Source == 'Cochin'):
                d_Cochin = 1
                d_Delhi = 0
                d_New_Delhi = 0
                d_Hyderabad = 0
                d_Kolkata = 0
            
            elif (Source == 'Delhi'):
                d_Cochin = 0
                d_Delhi = 1
                d_New_Delhi = 0
                d_Hyderabad = 0
                d_Kolkata = 0

            elif (Source == 'New_Delhi'):
                d_Cochin = 0
                d_Delhi = 0
                d_New_Delhi = 1
                d_Hyderabad = 0
                d_Kolkata = 0

            elif (Source == 'Hyderabad'):
                d_Cochin = 0
                d_Delhi = 0
                d_New_Delhi = 0
                d_Hyderabad = 1
                d_Kolkata = 0

            elif (Source == 'Kolkata'):
                d_Cochin = 0
                d_Delhi = 0
                d_New_Delhi = 0
                d_Hyderabad = 0
                d_Kolkata = 1

            else:
                d_Cochin = 0
                d_Delhi = 0
                d_New_Delhi = 0
                d_Hyderabad = 0
                d_Kolkata = 0

            # print(
            #     d_Cochin,
            #     d_Delhi,
            #     d_New_Delhi,
            #     d_Hyderabad,
            #     d_Kolkata
            # )
            

        #     ['Total_Stops', 'Journey_day', 'Journey_month', 'Dep_hour',
        #    'Dep_min', 'Arrival_hour', 'Arrival_min', 'Duration_hours',
        #    'Duration_mins', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
        #    'Airline_Jet Airways', 'Airline_Jet Airways Business',
        #    'Airline_Multiple carriers',
        #    'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
        #    'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy',
        #    'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai',
        #    'Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad',
        #    'Destination_Kolkata', 'Destination_New Delhi']
            
            prediction=model.predict([[
                Total_stops,
                Journey_day,
                Journey_month,
                Dep_hour,
                Dep_min,
                Arrival_hour,
                Arrival_min,
                dur_hour,
                dur_min,
                Air_India,
                GoAir,
                IndiGo,
                Jet_Airways,
                Jet_Airways_Business,
                Multiple_carriers,
                Multiple_carriers_Premium_economy,
                SpiceJet,
                Trujet,
                Vistara,
                Vistara_Premium_economy,
                s_Chennai,
                s_Delhi,
                s_Kolkata,
                s_Mumbai,
                d_Cochin,
                d_Delhi,
                d_Hyderabad,
                d_Kolkata,
                d_New_Delhi
            ]])

            output=round(prediction[0],2)
            # return HttpResponse(output)
            return render(request,'predict.html',{'flight':flight_form,"prediction_text":output})
       
    return render(request,'flight.html',{'flight':flight_form})
