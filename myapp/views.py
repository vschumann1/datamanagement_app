# myapp/views.py

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import GSL_grouped_ISK_2022, bruecken_ISK_2022, tunnel_ISK_2022, weichen_ISK_2022, stuetzauwerke_ISK_2022, schallschutzwaende_ISK_2022, bahnuebergaenge_ISK_2022, stationen_ISK_2022 
from django.core.paginator import Paginator
from .filters import GSLFilter
import plotly.express as px
import plotly.graph_objects as go
import json
import pandas as pd
import csv
from django.utils.safestring import mark_safe
import numpy as np
from .forms import MultiSelectFilterForm 
from django.db.models import Sum, Count
from shapely.geometry import LineString, MultiLineString #checken!
from shapely import wkt

mapbox_access_token = 'pk.eyJ1IjoiYW5ka29jaDkzIiwiYSI6ImNsMTZiNnU4dTE5MzQzY3MwZnV1NjVqOGoifQ.ZxCDeRkr59lifDEm4PIWQA'




def get_model_fields(model):
    return [field for field in model._meta.get_fields() if field.concrete and not field.name.startswith('_')]



def analysis_view(request):

  
        
    filters = GSLFilter(request.GET, queryset=GSL_grouped_ISK_2022.objects.all())
    gsllist = filters.qs

    model_data = {}
    streckennummer = request.GET.get('STR_NR', '')
    counts = {}
    sums = {}

    form = MultiSelectFilterForm(request.GET or None)

    option_to_model = {
        'Brücken': bruecken_ISK_2022,
        'Tunnel': tunnel_ISK_2022,
        'Weichen': weichen_ISK_2022,
        'Stützbauwerke': stuetzauwerke_ISK_2022,
        'Schallschutzwände': schallschutzwaende_ISK_2022,
        'Bahnübergänge': bahnuebergaenge_ISK_2022
    }
    

    if form.is_valid():
        selected_options = form.cleaned_data['selected_options']
        selected_bundeslaender = form.cleaned_data['selected_bundeslaender']

        filtered_ids = gsllist.values_list('STR_NR', flat=True)

        for option, model in option_to_model.items():
            if option in selected_options:
                queryset = model.objects.filter(gsl_grouped_isk_2022__STR_NR__in=filtered_ids)
                if selected_bundeslaender:
                    queryset = queryset.filter(LAND__in=selected_bundeslaender)

                counts[option] = queryset.count()

                # Calculate sums for specific columns based on the model
                if option == 'Brücken':
                    sums['Fläche Brücken'] = queryset.aggregate(Sum('FLAECHE'))['FLAECHE__sum'] or 0
                elif option in ['Tunnel', 'Stützbauwerke', 'Schallschutzwände']:
                    sum_key = f'Länge {option}'
                    sums[sum_key] = int((queryset.aggregate(Sum('LAENGE'))['LAENGE__sum'] or 0)/1000)

                # Define 'fields' before using it
                fields = [field.name for field in model._meta.fields if field.name != 'geometry']
                paginator = Paginator(queryset, 5)
                page_number = request.GET.get(f'page_{option}')
                page_obj = paginator.get_page(page_number)

                
                items_data = []
                for item in queryset:
                    item_fields = {}
                    for field in fields:  
                        item_fields[field] = getattr(item, field, "N/A")
                    items_data.append(item_fields)

                
                model_data[option] = {
                    'items_data': items_data,  
                    'fields': fields,  
                    'page_obj': paginator.get_page(page_number), 
                }



    if 'download-csv' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="filtered_data.csv"'

        writer = csv.writer(response)
        fields = [field for field in GSL_grouped_ISK_2022._meta.get_fields() if field.concrete]
        writer.writerow([field.name for field in fields])

        for obj in gsllist:
            writer.writerow([getattr(obj, field.name) for field in fields])

        return response

    if 'download-excel' in request.GET:
        df = pd.DataFrame(list(gsllist.values(*[field.name for field in GSL_grouped_ISK_2022._meta.get_fields() if field.concrete])))
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="filtered_data.xlsx"'
        df.to_excel(response, index=False)

        return response
    
    for category, model in option_to_model.items():
        if f'download-csv-{category}' in request.GET:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{category}_data.csv"'
            writer = csv.writer(response)
            queryset = model.objects.filter(gsl_grouped_isk_2022__STR_NR__in=gsllist.values_list('STR_NR', flat=True))
            fields = [field for field in model._meta.get_fields() if field.concrete and field.name != 'geometry']
            writer.writerow([field.name for field in fields])
            for obj in queryset:
                writer.writerow([getattr(obj, field.name) for field in fields])
            return response

        if f'download-excel-{category}' in request.GET:
            queryset = model.objects.filter(gsl_grouped_isk_2022__STR_NR__in=gsllist.values_list('STR_NR', flat=True))
            df = pd.DataFrame(list(queryset.values(*[field.name for field in model._meta.get_fields() if field.concrete and field.name != 'geometry'])))
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{category}_data.xlsx"'
            df.to_excel(response, index=False)
            return response
        

    all_bridges = bruecken_ISK_2022.objects.filter(gsl_grouped_isk_2022__in=gsllist).distinct()
    all_strecken = gsllist
    all_bahnuebergaenge =  bahnuebergaenge_ISK_2022.objects.filter(gsl_grouped_isk_2022__in=gsllist).distinct()
    all_weichen = weichen_ISK_2022.objects.filter(gsl_grouped_isk_2022__in=gsllist).distinct()
    all_tunnel = tunnel_ISK_2022.objects.filter(gsl_grouped_isk_2022__in=gsllist).distinct()
  
    df_all_strecken = pd.DataFrame(all_strecken.values())
    try:

        df_all_strecken["geometry"] = df_all_strecken["geometry"].apply(wkt.loads)
    except KeyError:
        df_all_strecken = pd.DataFrame(columns = list(df_all_strecken.columns))
    
    df_all_bahnuebergaenge = pd.DataFrame(all_bahnuebergaenge.values())

    df_all_weichen = pd.DataFrame(all_weichen.values())
    
    df_all_tunnel = pd.DataFrame(all_tunnel.values())
    try:

        df_all_tunnel["geometry"] = df_all_tunnel["geometry"].apply(wkt.loads)
    except KeyError:
        df_all_tunnel = pd.DataFrame(columns = list(df_all_tunnel.columns))
    #print(df_all_strecken)

    try:
        hover_text_bu = df_all_bahnuebergaenge.apply(lambda row: f"REGION: {row['REGION']}<br>NETZ: {row['NETZ']}<br>LAGE_KM: {row['LAGE_KM']}", axis=1) #STR_NR
            
        # Für Brücken (df_br_new)
        hover_text_br = [
            f"LAND: {bridge.LAND}<br>EIU: {bridge.EIU}<br>REGION: {bridge.REGION}<br>NETZ: {bridge.NETZ}<br>"
            f"ANLAGEN_NR: {bridge.ANLAGEN_NR}<br>ANLAGEN_UNR: {bridge.ANLAGEN_UNR}<br>"
            f"VON_KM: {bridge.VON_KM}<br>BIS_KM: {bridge.BIS_KM}<br>VON_KM_I: {bridge.VON_KM_I}<br>"
            f"BIS_KM_I: {bridge.BIS_KM_I}<br>RIKZ: {bridge.RIKZ}<br>RIL_100: {bridge.RIL_100}<br>"
            f"STR_MEHRFACHZUORD: {bridge.STR_MEHRFACHZUORD}<br>FLAECHE: {bridge.FLAECHE}<br>"
            f"BR_BEZ: {bridge.BR_BEZ}<br>BAUART: {bridge.BAUART}<br>BESCHREIBUNG: {bridge.BESCHREIBUNG}<br>"
            f"ZUST_KAT: {bridge.ZUST_KAT}<br>WL_SERVICEEINR: {bridge.WL_SERVICEEINR}<br>Match: {bridge.Match}"
            for bridge in all_bridges
        ]


        # Für Tunnel (df_tu_new)
        hover_text_tu = df_all_tunnel.apply(lambda row: f"REGION: {row['REGION']}<br>NETZ: {row['NETZ']}<br>VON_KM: {row['VON_KM']}<br>BIS_KM: {row['BIS_KM']}<br>LAENGE: {row['LAENGE']}<br>BAUWEISE: {row['BAUWEISE']}", axis=1)

        hover_text_strecke = df_all_strecken.apply(lambda row: f"REGION: {row['REGION']}<br>NETZ: {row['NETZ']}<br>STR_NR: {row['STR_NR']}<br>VON_KM: {row['VON_KM']}<br>BIS_KM: {row['BIS_KM']}<br>LAENGE: {row['LAENGE']}", axis=1)

        hover_text_weiche = df_all_weichen.apply(lambda row: f"REGION: {row['REGION']}<br>NETZ: {row['NETZ']}<br>LAGE_KM: {row['LAGE_KM']}", axis=1) #STR_NR



        fig = go.Figure()

        

        # Datainklusion 4 
        lons_str = []
        lats_str = []
        hover_texts_str = []

        for index, row in df_all_strecken.iterrows():
            geom_str = (row['geometry'])
            print(type(geom_str))
            # Check if the geometry is a LineString
            if isinstance(geom_str, LineString):
                xs, ys = geom_str.xy
                lons_str.extend(xs.tolist() + [None])  # Add None at the end of each linestring
                lats_str.extend(ys.tolist() + [None])
            # Check if the geometry is a MultiLineString
            elif isinstance(geom_str, MultiLineString):
                print("test")
                for line in geom_str.geoms:  # Use .geoms to iterate over each LineString
                    xs, ys = line.xy
                    lons_str.extend(xs.tolist() + [None])  # Add None at the end of each linestring
                    lats_str.extend(ys.tolist() + [None])
                
               
            # Add hover text for each segment - this needs adjustment to prevent reference errors
            if 'xs' in locals():
                hover_texts_str.extend(hover_text_strecke)
            
       
        
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=lons_str,
            lat=lats_str,
            hovertext=hover_texts_str,
            hoverinfo="text",
            line=dict(color='#edb7ea', width=3),
            name='Strecke',
            showlegend=True,
        ))
        # Datainklusion 2

        fig.add_trace(go.Scattermapbox(
            lat=[bridge.GEOGR_BREITE for bridge in all_bridges if bridge.GEOGR_BREITE is not None],
            lon = [bridge.GEOGR_LAENGE for bridge in all_bridges if bridge.GEOGR_LAENGE is not None],
            mode='markers',
            marker=dict(size=7, color='#006587'),
            hoverinfo='text',
            hovertext=hover_text_br,
            name='Brücken',
            showlegend=True,
        ))


        #Bahnübergänge
        fig.add_trace(go.Scattermapbox(
            lat=df_all_bahnuebergaenge['breite'],
            lon=df_all_bahnuebergaenge['laenge'],
            mode='markers',
            marker=dict(size=7, color='#68DAFF'),
            hoverinfo='text',
            hovertext=hover_text_bu,
            name='Bahnübergänge',
            showlegend=True,
        ))

        fig.add_trace(go.Scattermapbox(
            lat=df_all_weichen['lat'],
            lon=df_all_weichen['lon'],
            mode='markers',
            marker=dict(size=7, color='#eb3f3f'),
            hoverinfo='text',
            hovertext=hover_text_weiche,
            name='Weiche',
            showlegend=True,
        ))

        lons = []
        lats = []
        hover_texts = []

        for index, row in df_all_tunnel.iterrows():
            geom = row['geometry']
            # Check if the geometry is a LineString
            if isinstance(geom, LineString):
                xs, ys = geom.xy
                lons.extend(xs.tolist() + [None])  # Add None at the end of each linestring
                lats.extend(ys.tolist() + [None])
            # Check if the geometry is a MultiLineString
            elif isinstance(geom, MultiLineString):
                for line in geom.geoms:  # Use .geoms to iterate over each LineString
                    xs, ys = line.xy
                    lons.extend(xs.tolist() + [None])  # Add None at the end of each linestring
                    lats.extend(ys.tolist() + [None])
            # Add hover text for each segment - this needs adjustment to prevent reference errors
            if 'xs' in locals():
                hover_texts.extend(hover_text_tu)


        # Add a single trace for all tunnel line segments
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=lons,
            lat=lats,
            hovertext=hover_texts,
            hoverinfo="text",
            line=dict(color='#5496B8', width=7),
            name='Tunnel',  
            showlegend=True,
        ))


        # Datainklusion 3 

        # Calculate the mean of the latitudes and longitudes
        lats_series = pd.Series(lats)
        lons_series = pd.Series(lons)
        
        lons_series_str = pd.Series(lons_str)
        lats_series_str = pd.Series(lats_str)
        
        # Now, concatenate using pandas Series
        all_longitudes = pd.concat([lons_series_str, lons_series, df_all_bahnuebergaenge['laenge']])
        all_latitudes = pd.concat([lats_series_str, lats_series, df_all_bahnuebergaenge['breite']])

        lat1 = np.mean(all_latitudes)
        lon1 = np.mean(all_longitudes)
        # Continue with updating the layout and showing the figure as before
        fig.update_layout(
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center={"lat": lat1, "lon": lon1},
                zoom=5.5,
                style='outdoors'
            ),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            ),
            title="Geoplot Strecken, Weichen, Bahnübergänge, Brücken und Tunnel",
            title_font=dict(color='#003366', size=24),
            title_x=0.5,
            margin=dict(b=40),
        )

        
        # COPY for later 


        fig.update_layout(
        mapbox=dict(
        accesstoken=mapbox_access_token,
        center={"lat": lat1, "lon": lon1},
        zoom=9.0,
        style='outdoors'
        ),
        legend=dict(
        font=dict(
            size=20  
        )
        ),

        
        #Slider für Zoom
        
        
        
        # Title-Bezeichnung
        
        showlegend=True,
        title_text="",
        title_font=dict(size=24, color="#003366"),
        title_pad=dict(t=20, b=20),
        
        # Dropdown für Map-Ansicht
        updatemenus=[dict(
        buttons=[
            dict(args=[{"mapbox.style": "outdoors"}],
                label="Outdoors",
                method="relayout"),
            dict(args=[{"mapbox.style": "satellite"}],
                label="Satellite",
                method="relayout"),
            dict(args=[{"mapbox.style": "light"}],
                label="Hell",
                method="relayout"),
            dict(args=[{"mapbox.style": "dark"}],
                label="Dunkel",
                method="relayout"),
            dict(args=[{"mapbox.style": "streets"}],
                label="Straße",
                method="relayout"),
            dict(args=[{"mapbox.style": "satellite-streets"}],
                label="Satellite mit Straßen",
                method="relayout"),
        ],
        direction="down",
        pad={"r": 10, "t": 10},
        showactive=True,
        x=1,
        xanchor="right",
        y=1.1,
        yanchor="top",
        bgcolor="#001C4F",
        font=dict(size=15, color="white")  
        )]
        )

        fig.update_layout(height=800)

        plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    except KeyError as error:
        print(error)
        no_data_message = "Für diese Streckennummer ist keine Geo-Visualisierung verfügbar."
        plot_html = mark_safe(f"<div style='text-align: center; padding: 20px;'>{no_data_message}</div>")



    paginator = Paginator(gsllist, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

     # Retrieve the list of columns to exclude from the request
    exclude_columns = ['geometry']



    # Filter out the excluded columns
    fields = [field for field in GSL_grouped_ISK_2022._meta.get_fields() if field.concrete and field.name not in exclude_columns]

    #print("Model data:", model_data)

    context = {
        'page_obj': page_obj,
        'fields': fields,
        'filters': filters,
        'form': form,
        'model_data': model_data,
        'streckennummer': streckennummer,
        'counts': counts,
        'sums': sums,
        'plot_html': plot_html,
        
    }


    return render(request, 'myapp/analysis.html', context)


def hlk_view(request):
    data = [
        {'lat': 40.7128, 'lon': -74.0060, 'name': 'New York'},
        {'lat': 34.0522, 'lon': -118.2437, 'name': 'Los Angeles'},
        # Add more data points as needed
    ]

    # Convert your data into a DataFrame or use your existing DataFrame
    df = pd.DataFrame(data)

    # Create a Plotly Express map
    fig = px.scatter_geo(df,
                         lat='lat',
                         lon='lon',
                         hover_name='name',  # Displays the 'name' value on hover
                         projection="natural earth")

    # Convert the figure to HTML and JavaScript code
    plot_div = fig.to_html(full_html=False)

    # Pass the plot to the template
    context = {'plot_div': plot_div}
    return render(request, 'myapp/hlk.html', context)

def main_view(request):
    return render(request, 'myapp/main.html')

def geo_view(request):
    return render(request, 'myapp/geo.html')

def pb_view(request):
    stations_list = stationen_ISK_2022.objects.all()
    paginator = Paginator(stations_list, 10)  # Show 10 stations per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'myapp/personenbahnhoefe.html', {'page_obj': page_obj})

def station_detail(request, station_number):
    station = get_object_or_404(stationen_ISK_2022, number=station_number)
    return render(request, 'myapp/pb_detail.html', {'station': station})


