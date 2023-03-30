import pandas as pd
import geopandas as gpd
import folium
import sys
import json
from branca.element import Template, MacroElement
import numpy as np
import sys

# # exemple de legende dégradée
# import branca
# colormap = branca.colormap.linear.YlOrRd_09.scale(0, 8500)
# colormap = colormap.to_step(index=[0, 1000, 3000, 5000, 8500])
# colormap.caption = 'Incidents of Crime in Victoria (year ending June 2018)'
# colormap.add_to(m)


def all_vues():
    dico_colonnes ={
        'adedpe202006_logtype_baie_mat':'Baies vitrees - materiaux'
        ,'adedpe202006_logtype_baie_type_vitrage':'Baies vitrees - type vitrage'
        ,'adedpe202006_logtype_baie_u':'Baies vitrees - conductivite thermique u'
        #,'adedpe202006_logtype_mur_ep_mat_ext'
        # ,'materiau_mur_ext':'Murs extéreurs - matériaux'->optionnel
        ,'adedpe202006_logtype_mur_mat_ext':'Murs exterieurs - materiaux detail'
        ,'adedpe202006_logtype_mur_pos_isol_ext':'Murs exterieurs - type isolation'
        ,'adedpe202006_logtype_mur_u_ext':'Murs exterieurs : conductivite thermique u'
        ,'materiau_plancher': 'Plancher - materiaux'
        #,'adedpe202006_logtype_pb_mat'
        ,'adedpe202006_logtype_pb_pos_isol':'Plancher - type isolation'
        ,'adedpe202006_logtype_pb_u':'Plancher : conductivite thermique u'
        , 'adedpe202006_logtype_perc_surf_vitree_ext' :'Baies vitrees - pourcentage surface'
        ,'adedpe202006_logtype_periode_construction':'Periode de construction'
        # ,'materiau_plafond':'Plafond - matériaux'->optionnel
        ,'adedpe202006_logtype_ph_mat':'Plafond - materiaux detail'
        ,'adedpe202006_logtype_ph_pos_isol':'Plafond - type isolation'
        ,'adedpe202006_logtype_ph_u':'Plafond : conductivite thermique u'
        # ,'cerffo2020_annee_construction' -> regroupement dans période constuction
        # ,'materiau_mur' : 'Murs extérieurs - matériaux princ'->optionnel
        ,'cerffo2020_mat_mur_txt': 'Murs exterieurs - materiaux princ detail'
        ,'cerffo2020_mat_toit_txt':'Toiture - materiaux detail'
        ,'adedpe202006_logtype_nom_methode_dpe': 'DPE- methode'
        # ,'adedpe202006_logtype_ch_type_ener_corr': 'Chauffage - énergie'->optionnel
        ,'adedpe202006_logtype_classe_conso_ener':'DPE - conso'
        ,'adedpe202006_logtype_classe_estim_ges':'DPE - ges'
        # ,'adedpe202006_logtype_conso_ener' -> continue, en classe ci-dessus
        #,'adedpe202006_logtype_date_reception_dpe' -> à regrouper
        # ,'ecs_type_ener' : 'ECS- énergie'->optionnel
        #,'adedpe202006_logtype_estim_ges' -> continue, en classe ci-dessus
        ,'adedpe202006_logtype_inertie':'DPE - inertie'
        # ,'adedpe202006_logtype_min_classe_ener_ges':'DPE - ges min'->optionnel
        ,'chauffage_principal':'Chauffage - principal'
        # ,'adedpe202006_logtype_ch_is_solaire' : 'Chauffage - solaire'->optionnel
        ,'adedpe202006_logtype_ch_type_inst' : 'Chauffage - collectif'
        ,'ecs_principal':'ECS - principal'
        # ,'adedpe202006_logtype_ecs_is_solaire': 'ECS - solaire'->optionnel
        ,'adedpe202006_logtype_ecs_type_inst' : 'ECS - collectif'
        ,'adedpe202006_logtype_presence_balcon': 'balcon - presence'
        ,'adedpe202006_logtype_presence_climatisation':'climatisation - presence'
        ,'cluster_12':'Clustering complet'
        ,'interpretation_cluster_12':'Clustering interpretation'
    }
    return dico_colonnes


def set_couleurs():
    couleurs=['red','darkgreen','yellow','blue',\
        'darkorange','darkkhaki','peru','darkcyan','fuchsia','chartreuse','silver','grey','black', 'lime','orange','khaki','whitesmoke']    
    return couleurs

def get_highlight(couleur):
    # style={'orange':'red','green':'darkgreen','yellow':'gold','skyblue':'blue','khaki':'darkkhaki',\
        # 'bisque':'darkorange','linen':'peru','darkcyan':'cyan' }
    style={'red':'orange','darkgreen':'lime','yellow':'gold','blue':'skyblue',\
        'darkorange':'bisque','darkkhaki':'khaki','peru':'linen','darkcyan':'cyan','fuchsia':'orchid','chartreuse':'greenyellow','silver':'lightgrey','grey':'darkgrey',\
             'black':'grey', 'lime':'darkgreen','orange':'red','khaki':'darkkhaki','whitesmoke':'silver'}
    return style[couleur]


def tooltip_tableau_html():
    i = row
    institution_name=df['INSTNM'].iloc[i] 
    institution_url=df['URL'].iloc[i]
    institution_type = df['CONTROL'].iloc[i] 
    highest_degree=df['HIGHDEG'].iloc[i] 
    city_state = df['CITY'].iloc[i] +", "+ df['STABBR'].iloc[i]                     
    admission_rate = df['ADM_RATE'].iloc[i]
    cost = df['COSTT4_A'].iloc[i]
    instate_tuit = df['TUITIONFEE_IN'].iloc[i]
    outstate_tuit = df['TUITIONFEE_OUT'].iloc[i]

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
<html>
<head>
<h4 style="margin-bottom:10"; width="200px">{}</h4>""".format(institution_name) + """
</head>
    <table style="height: 126px; width: 350px;">
<tbody>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Institution Type</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(institution_type) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Institution URL</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(institution_url) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">City and State</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(city_state) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Highest Degree Awarded</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(highest_degree) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Admission Rate</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(admission_rate) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Annual Cost of Attendance $</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(cost) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">In-state Tuition $</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(instate_tuit) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Out-of-state Tuition $</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(outstate_tuit) + """
</tr>
</tbody>
</table>
</html>
"""
    return html


def viz_batiment_unique(vue,bat,couleur,liste_active,display_clustering):
    return bat.T.apply(lambda x : process_batiment_unique(vue,x,couleur,liste_active,display_clustering))

def process_batiment_unique(vue,bat,couleur,liste_active,display_clustering):
    dico_colonnes=all_vues()
    dico_colonnes=dict(sorted(dico_colonnes.items(), key=lambda item: item[1]))
    variables = list(dico_colonnes.keys())
    labels=(list(dico_colonnes.values()))

    var_tooltip=[variables[labels.index(i)] for i in liste_active]

    
    if(display_clustering):
        mytooltip=folium.features.GeoJsonTooltip(
                fields=['interpretation_cluster_12'],
                aliases=['Clustering:'],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
                )
    else: 
        mytooltip=folium.features.GeoJsonTooltip(
                fields=var_tooltip,
                aliases=liste_active,
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
                )
       

    geo_j = bat.to_json()
    geo_style_function = lambda x: {'color' :  couleur,'opacity' : 0.50,'weight' : 2,}
    geo_highlight_function = lambda x: {'color': get_highlight(couleur), 'opacity' : 0.9,'weight': 4,'dashArray' : '3, 6'}
    # desc_html='aaaaaa'
    # main display function using the two previous functions
    geo = folium.features.GeoJson(
    data=geo_j,
    name = 'geo',
    control = True,
    style_function = geo_style_function, 
    highlight_function = geo_highlight_function,

    # the tooltip is where the info display happens
    # using "folium.features.GeoJsonTooltip" function instead of basic text tooltip
            # tooltip=folium.features.GeoJsonTooltip(
            #     fields=[
            #         'bnb_id',
            #         vue, 
            #     ],
            #     # fields=list(bat.columns)[3:5],
            #     aliases=[
            #         "Identifiant: ",
            #         "Filtre: ",
            #     ],
            #     style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
            #     )
             tooltip=mytooltip,
            # tooltip=folium.map.Tooltip(
            #         text=folium.Html(desc_html, script=True, width=300).render(),
            # )
    )

    return geo


def viz_batiment(vue,bat,couleur,liste_active,display_clustering):

    dico_colonnes=all_vues()
    dico_colonnes=dict(sorted(dico_colonnes.items(), key=lambda item: item[1]))
    variables = list(dico_colonnes.keys())
    labels=(list(dico_colonnes.values()))

    var_tooltip=[variables[labels.index(i)] for i in liste_active]


    
    if(display_clustering):
        mytooltip=folium.features.GeoJsonTooltip(
                fields=['interpretation_cluster_12'],
                aliases=['Clustering:'],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
                )
    else: 
        mytooltip=folium.features.GeoJsonTooltip(
                fields=var_tooltip,
                aliases=liste_active,
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
                )

    geo_j = bat.to_json()
    geo_style_function = lambda x: {'color' :  couleur,'opacity' : 0.50,'weight' : 2,}
    geo_highlight_function = lambda x: {'color': get_highlight(couleur), 'opacity' : 0.9,'weight': 4,'dashArray' : '3, 6'}
    # desc_html='aaaaaa'
    # main display function using the two previous functions
    geo = folium.features.GeoJson(
    data=geo_j,
    name = 'geo',
    control = True,
    style_function = geo_style_function, 
    highlight_function = geo_highlight_function,

    # the tooltip is where the info display happens
    # using "folium.features.GeoJsonTooltip" function instead of basic text tooltip
            # tooltip=folium.features.GeoJsonTooltip(
            #     fields=[
            #         'bnb_id',
            #         vue, 
            #     ],
            #     # fields=list(bat.columns)[3:5],
            #     aliases=[
            #         "Identifiant: ",
            #         "Filtre: ",
            #     ],
            #     style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
            #     )
             tooltip=mytooltip,
            # tooltip=folium.map.Tooltip(
            #         text=folium.Html(desc_html, script=True, width=300).render(),
            # )
    )

    return geo


def popup_batiment(bat_actif,clients,geo):
    next=0
    for _, r in clients.iterrows(): 
        #folium.Marker((r.noyau.y,r.noyau.x),icon=folium.Icon(color='green')).add_to(geo)
        try:
            html=f"""
            <h5>{'Identifiant Stonal : ' + r['code']+" : "+eval(r['assetData.ADDRESS'])[0].get('value')}</h5>
            """
            if(next<len(bat_actif)): 
                html=html+f"""
                <h5> {"identifiant BNB : "+bat_actif['bnb_id'].iloc[next]}</h5>
                """

            iframe = folium.IFrame(html=html, width=600, height=100)
            popup = folium.Popup(iframe, max_width=600)
            # popup.add_to(geo)

            #folium.Marker((r.noyau.y,r.noyau.x), popup=clients['code'].iloc[next]+","+eval(clients['assetData.ADDRESS'].iloc[next])[0].get('value')),icon=folium.Icon(color='green')).add_to(geo)
            # folium.Marker((r.noyau.y,r.noyau.x), popup=popup,icon=folium.Icon(color='green')).add_to(geo)
            folium.Marker((r.form_LAT,r.form_LNG), popup=popup,icon=folium.Icon(color='green')).add_to(geo)
        except:
            # sys.exit(0)
            continue
        next=next+1
        
    return geo

def popup_batiment_ancien(bat_actif,clients,geo):
    next=0
    for _, r in bat_actif.iterrows(): 
        #folium.Marker((r.noyau.y,r.noyau.x),icon=folium.Icon(color='green')).add_to(geo)
        try:
            html=f"""
            <h5>{'Identifiant Stonal : ' + clients['code'].iloc[next]+" : "+eval(clients['assetData.ADDRESS'].iloc[next])[0].get('value')}</h5>
            <h5> {"identifiant BNB : "+r['bnb_id']}</h5>
            """
            iframe = folium.IFrame(html=html, width=600, height=100)
            popup = folium.Popup(iframe, max_width=600)
            # popup.add_to(geo)

            #folium.Marker((r.noyau.y,r.noyau.x), popup=clients['code'].iloc[next]+","+eval(clients['assetData.ADDRESS'].iloc[next])[0].get('value')),icon=folium.Icon(color='green')).add_to(geo)
            # folium.Marker((r.noyau.y,r.noyau.x), popup=popup,icon=folium.Icon(color='green')).add_to(geo)
            folium.Marker((r.form_LAT,r.form_LNG), popup=popup,icon=folium.Icon(color='green')).add_to(geo)
        except:
            # sys.exit(0)
            continue
        next=next+1
        
    return geo


def set_legend(vue,legende):
    
    legende=sorted(legende, key=lambda x: (x is None, x))
    couleurs=set_couleurs()
    legend=f'''<body>
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
        border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
        
    <div class='legend-title'>{vue}</div>
    <div class='legend-scale'>
        <ul class='legend-labels'>
        '''
    
    i=0
    
    for c in legende:
        legend=legend+f'''<li><span style='background:{couleurs[i]};opacity:0.7;'></span>{c}</li>'''
        i=i+1
        if(i>16): i=0
   
    legend=legend+'''
  

        </ul>
    </div>
    </div>
    </body>
    '''





    deb_macro='''{% macro html(this, kwargs) %}
    '''
    fin_macro='''{% endmacro %}'''

    head = '''
    <head>
        <meta charset='utf-8'>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>jQuery UI Draggable - Default functionality</title>
        <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

        <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
        
        <script>
        $( function() {
        $( "#maplegend" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });

        </script>
    </head>

    '''



    css_options='''
    <style type='text/css'>
        .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
        .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
        .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
        .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
        .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
        .maplegend a {
        color: #777;
        }
    </style>
    '''



    template = f"""
    {deb_macro}
    <!doctype html>
    <html lang="fr">
    {head}
    {legend}
    </html>
    {css_options}
    {fin_macro} 

    """

    plot_legend = MacroElement()
    plot_legend._template = Template(template)



    return plot_legend



def display_vue(vue,bat_actif,df_batiment,clients,liste_active,jeu=0.015,dept=75):
    couleurs=set_couleurs()


    display_clustering=False
    for i in liste_active: 
        if(str(i).startswith('Clustering')): 
            display_clustering=True

    # xactif=float(bat_actif.iloc[0].noyau.x)
    # yactif=float(bat_actif.iloc[0].noyau.y)
    yactif=float(clients.iloc[0].form_LAT)
    xactif=float(clients.iloc[0].form_LNG)
    print(xactif, yactif)
    m = folium.Map(location=(yactif,xactif),min_zoom=0, max_zoom=18, zoom_start=16, tiles='CartoDB positron')

    #df_reduit=df_batiment[(df_batiment.noyau.x.between(xactif-jeu, xactif+jeu)) & (df_batiment.noyau.y.between(yactif-jeu, yactif+jeu))]
    #df_reduit=df_reduit[['bnb_id','geometry',vue]]

    # On essaie sans réduction sur les variables explicatives, 
    #on ne supprime que la colonne noyau qui donne une erreur dans le passage au geojson de la methoe viz_batiment
    # df_reduit=df_batiment[['bnb_id','geometry',vue]]
    # df_reduit=df_reduit[df_reduit.isnull().any(axis=1)==False]
    df_reduit=df_batiment.drop(['noyau'], axis=1)
    df_reduit=df_reduit[df_reduit[['bnb_id','geometry',vue]].isnull().any(axis=1)==False]
   
    legende=set_legend(all_vues()[vue],df_batiment[vue].unique())
    m.get_root().add_child(legende)

    i=0
    print(df_batiment[vue].unique)
    for p in sorted(df_reduit[vue].unique()):
        df_p=df_reduit[df_reduit[vue]==p]
        geo=viz_batiment(vue,df_p,couleurs[i],liste_active,display_clustering)
        i=i+1
        if(i>16): i=0
        geo.add_to(m)
    
    geo=popup_batiment(bat_actif,clients,geo)


    m.save('C:/Users/FilipeAfonso/Documents/ESG/map'+str(dept)+'.html')