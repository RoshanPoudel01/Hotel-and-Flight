from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from .models import Flight
from .forms import FlightForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from sklearn.preprocessing import LabelEncoder
import stripe
import pandas as pd
import numpy as np
import pickle
from bookings.models import FlightBooking
from django.conf import settings
import math 

# Create your views here.
def flightpredict(request):
    flight_form = FlightForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if flight_form.is_valid():
            source = flight_form.cleaned_data['source']
            destination = flight_form.cleaned_data['destination']
            arrival_date = flight_form.cleaned_data['arrival_date']
            departure_date = flight_form.cleaned_data['departure_date']
            airline = flight_form.cleaned_data['airline']
            stoppage = flight_form.cleaned_data['stoppage']

            # Check if the input matches a saved flight instance in the database
            flight = Flight.objects.filter(source=source, destination=destination, arrival_date=arrival_date, departure_date=departure_date, airline=airline, stoppage=stoppage).first()

            if flight:
                print("Price from db",flight.id)
                return render(request, 'predict.html', {'flight': flight_form, "prediction_text": flight.predicted_price,"flightid":flight.id})

            else:
                with open('flight_rf.pkl', 'rb') as f:
                    model = pickle.load(f)
                print(">>>",model)
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
                form=flight_form.save(commit=False)
                form.predicted_price=output
                form.save()
                flight = Flight.objects.filter(source=source, destination=destination, arrival_date=arrival_date, departure_date=departure_date, airline=airline, stoppage=stoppage).first()
                print("Price",flight.id)
                return render(request,'predict.html',{'flight':flight_form,"prediction_text":output,"flightid":flight.id})
       
    return render(request,'flight.html',{'flight':flight_form})
