import numpy as np
import pandas as pd

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column

from bokeh.models import Select, CheckboxButtonGroup ### Widgets

### Dataset Imports
import seaborn as sns

from sklearn.datasets import load_breast_cancer

from bokeh.palettes import Blues
from bokeh.models import BasicTicker, ColorBar, LinearColorMapper, PrintfTickFormatter, ContinuousColorMapper
from math import pi

checkbox_options = [
    'mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness'
]
attr_color_map = {
    'mean radius' : "dodgerblue",
    'mean texture': "tomato",
    'mean perimeter': "lime",
    'mean area': "orange",
    'mean smoothness': "pink",
}
color_mapping = {'malignant':"tomato", 'benign':"dodgerblue"}


#### Dataset Loading #####
data = load_breast_cancer()

df_bc = pd.DataFrame(data=data.data, columns=data.feature_names)
df_bc['type'] = data.target
df_bc['type'] = df_bc['type'].replace(0, data.target_names[0]).replace(1, data.target_names[1])


### Histogram Code Starts ###########

hists, edges = np.histogram(df_bc['mean radius'], density=True, bins=10)

histogram = figure(plot_width=600, plot_height=400, 
                   title="Data Histogram")

histogram.quad(top=hists, bottom=0,
               left=edges[:-1], 
               right=edges[1:], 
               legend_label='mean radius', 
               alpha=0.5)

histogram.xaxis.axis_label = 'mean radius'
histogram.yaxis.axis_label = 'Frequency'

histogram.legend.location = "top_left"

### Histogram Code Ends ###########


### Scatter Chart Code Starts ###########

scatter = figure(plot_width=500, plot_height=400,
                 title="Mean Radius vs Mean Texture")

for cls in ['malignant', 'benign']:
    scatter.circle(
        x=df_bc[df_bc["type"]==cls]["mean radius"],
        y=df_bc[df_bc["type"]==cls]["mean texture"],
        color=color_mapping[cls],
        size=10, 
        alpha=0.8,
        legend_label=cls,
    )

scatter.xaxis.axis_label= "mean radius".upper()
scatter.yaxis.axis_label= "mean texture".upper()

### Scatter Chart Code Ends ###########


### Heatmap Code Starts ###########

corr_matrix = df_bc.iloc[:, :-1].corr()

corr_index = list(corr_matrix.index)
corr_cols = list(corr_matrix.columns)

corr_matrix.index.name = 'level_0'
corr_matrix = corr_matrix.rename_axis('parameters', axis=1)

df_corr = pd.DataFrame(corr_matrix.stack(), columns=['correlation']).reset_index()
df_corr['correlation_percentage'] = ((df_corr['correlation']-(-1))/(1-(-1))) * 100

mapper = LinearColorMapper(palette=sns.color_palette('coolwarm', n_colors=256,).as_hex(), low=-1, high=1)

TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"
BOKEH_TOOLS = "hover,save,pan,reset,wheel_zoom,box_select,tap,undo,redo,zoom_in,zoom_out,crosshair"

heatmap = figure(title="Breast Cancer Correlation",
           x_range=corr_index, y_range=corr_cols,
           x_axis_location="above", width=1100, height=500,
           tools=BOKEH_TOOLS, toolbar_location='below',
           tooltips=[('relation', '@level_0 - @parameters'), ('coef', '@correlation')])

heatmap.grid.grid_line_color = None
heatmap.axis.axis_line_color = None
heatmap.axis.major_tick_line_color = None
heatmap.axis.major_label_text_font_size = "7px"
heatmap.axis.major_label_standoff = 0
heatmap.xaxis.major_label_orientation = pi / 3

heatmap.rect(x="level_0", y="parameters", width=1, height=1,
       source=df_corr,
       fill_color={'field': 'correlation', 'transform': mapper},
       line_color=None)

# colorbar
color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="7px",
                     ticker=BasicTicker(desired_num_ticks=10),
                     formatter=PrintfTickFormatter(format="%.1f"),
                     label_standoff=6, border_line_color=None)

heatmap.add_layout(color_bar, 'right')

### Heatmap Code Ends ###########


### Widgets Code Starts ################################

drop_scat1 = Select(title="X-Axis-Dim",
                    options=checkbox_options,
                    value=checkbox_options[0],
                    width=200)

drop_scat2 = Select(title="Y-Axis-Dim",
                    options=checkbox_options,
                    value=checkbox_options[1],
                    width=200)

checkbox_grp = CheckboxButtonGroup(labels=checkbox_options, active=[0], button_type="success")

### Widgets Code Ends ################################


##### Code to Update Charts as Per Widget  State Starts #####################

def update_histogram(attrname, old, new):
    '''
        Code to update Histogram as Per Check Box Selection
    '''
    
    histogram = figure(plot_width=600, plot_height=400, 
                       title="Data Histogram")
    
    attr_color_map = {
        'mean radius' : "dodgerblue",
        'mean texture': "tomato",
        'mean perimeter': "lime",
        'mean area': "orange",
        'mean smoothness': "pink",
    }

    for option in checkbox_grp.active:
        
        hists, edges = np.histogram(df_bc[checkbox_options[option]], density=True, bins=10)
        
        histogram.quad(top=hists, bottom=0,
                   left=edges[:-1], 
                   right=edges[1:], 
                   legend_label=checkbox_options[option], 
                   alpha=0.5)

    histogram.xaxis.axis_label = 'mean radius'
    histogram.yaxis.axis_label = 'Frequency'

    histogram.legend.location = "top_left"

    layout_with_widgets.children[0].children[0].children[1] = histogram


def update_scatter(attrname, old, new):
    '''
        Code to update Scatter Chart as Per Dropdown Selections
    '''
    
    scatter = figure(plot_width=500, plot_height=400,
                     title="%s vs %s Scatter Plot"%(drop_scat1.value.upper(), drop_scat2.value.upper()))

    color_mapping = {'malignant':"tomato", 'benign':"dodgerblue"}
    
    for cls in ['malignant', 'benign']:
        scatter.circle(
            x=df_bc[df_bc["type"]==cls][drop_scat1.value],
            y=df_bc[df_bc["type"]==cls][drop_scat2.value],
            color=color_mapping[cls],
            size=10, 
            alpha=0.8,
            legend_label=cls,
        )

    scatter.xaxis.axis_label= drop_scat1.value.upper()
    scatter.yaxis.axis_label= drop_scat2.value.upper()
    
    layout_with_widgets.children[0].children[1].children[1] = scatter #.children[1]


##### Code to Update Charts as Per Widget State Ends #####################


#### Registering Widget Attribute Change with Methods Code Starts ############# 
checkbox_grp.on_change("active", update_histogram)

drop_scat1.on_change("value", update_scatter)
drop_scat2.on_change("value", update_scatter)

#### Registering Widget Attribute Change with Methods Code Ends #############

####### Widgets Layout #################

layout_with_widgets = column(
                            row(
                                column(checkbox_grp, histogram),
                                column(row(drop_scat1, drop_scat2), scatter),
                            ),
                                column(heatmap)
                            )


############ Creating Dashboard ################
curdoc().add_root(layout_with_widgets)