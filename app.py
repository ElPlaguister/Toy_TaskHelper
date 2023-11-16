import gradio as gr
from gradio.themes.utils import colors
from utils import *
from task import *

def prepare_theme():
    theme = gr.themes.Default(primary_hue=colors.gray, 
                            secondary_hue=colors.emerald,
                            neutral_hue=colors.emerald).set(
        body_background_fill="*primary_800",
        body_background_fill_dark="*primary_800",
        
        block_background_fill="*primary_700",
        block_background_fill_dark="*primary_700",
        
        border_color_primary="*secondary_300",
        border_color_primary_dark="*secondary_300",
        
        block_border_width="3px",
        input_border_width="2px",
        
        input_background_fill="*primary_700",
        input_background_fill_dark="*primary_700",
        
        background_fill_primary="*neutral_950",
        background_fill_primary_dark="*neutral_950",
        
        background_fill_secondary="*primary_700",
        background_fill_secondary_dark="*primary_700",
        
        body_text_color="white",
        body_text_color_dark="white",
        
        block_label_text_color="*secondary_300",
        block_label_text_color_dark="*secondary_300",
        
        block_label_background_fill="*primary_800",
        block_label_background_fill_dark="*primary_800",
        
        color_accent_soft="*primary_600",
        color_accent_soft_dark="*primary_600",
    )
    return theme

manager = TaskManager()

def submit(namebox, tags, priority, time_options, start_date, start_time, end_date, end_time, repeat_options, repeat_value, repeat_unit, repeat_end_date, repeat_end_time):
    app = TaskApplication()
    app.name = namebox
    app.tags = tags
    app.priority = priority
    
    app.allow_time_specification = 'allow time specification' in time_options
    if app.allow_time_specification:
        app.use_start_time = 'use start time' in time_options
        app.use_end_time = 'use end time' in time_options
        if app.use_start_time:
            app.start_date = make_date(start_date)
            app.start_time = make_time(start_time)
        if app.use_end_time:
            app.end_date = make_date(end_date)
            app.end_time = make_time(end_time)
    
    app.allow_repeat = 'allow repeat' in repeat_options
    if app.allow_repeat:
        app.repeat_unit = repeat_unit
        app.repeat_value = repeat_value
        app.infinite = 'infinite' in repeat_options
        if not app.infinite:
            app.repeat_end_date = make_date(repeat_end_date)
            app.repeat_end_time = make_time(repeat_end_time)
            
    manager.enroll(app)
    return manager.dataframe
        

with gr.Blocks(theme=prepare_theme()) as demo:
    with gr.Tabs():
        with gr.Tab(label="Task Insertion"):
            with gr.Column():
                with gr.Row():
                    namebox = gr.Textbox(value="태스크 명을 입력하세요", interactive=True, label='Name', show_label=True, scale=5)
                    submit_button = gr.Button('태스크 생성', interactive=True)
                with gr.Row():
                    tags = gr.Dropdown(['Coursework', 'Daily Quest', 'Game', 'Project', 'Habby', 'Meeting', 'Seminar', 'Sleep'], multiselect=True, allow_custom_value=True, label='Tags', scale=4)
                    priority = gr.Slider(0, 1, 0.5, label='Priority', interactive=True)
                    
                with gr.Tabs():
                    # Start Time
                    with gr.Tab(label='Time'):
                        with gr.Column():
                            time_options = gr.CheckboxGroup(choices=['allow time specification', 'use start time', 'use end time'], value=['use start time', 'use end time'], show_label=False, interactive=True)
                            with gr.Row():
                                with gr.Row():
                                    start_date = gr.Textbox("2023년 11월 16일", interactive=True, label='Start Date')
                                    start_time = gr.Textbox("00:00", interactive=True, label='Time')
                                # End Time
                                with gr.Row():
                                    end_date = gr.Textbox("2023년 11월 16일", interactive=True, label='End Date')
                                    end_time = gr.Textbox("00:00", interactive=True, label='Time')
                    with gr.Tab(label='Repeat'):
                        repeat_options = gr.CheckboxGroup(choices=['allow repeat', 'infinite'], show_label=False)
                        with gr.Row():
                            with gr.Row():
                                repeat_value = gr.Textbox(value='1', interactive=True)
                                repeat_unit = gr.Dropdown(choices=['초마다', '분마다', '시간마다', '일마다', '주마다', '달마다', '년마다'], value='일마다', interactive=True)
                            with gr.Row():
                                repeat_end_date = gr.Textbox("2023년 11월 16일", interactive=True, label='End Date')
                                repeat_end_time = gr.Textbox("00:00", interactive=True, label='Time')
                
        with gr.Tab(label="Task Viewer"):
            with gr.Column():
                df = gr.Dataframe(manager.dataframe)
                
        submit_button.click(submit, [namebox, tags, priority, time_options, start_date, start_time, end_date, end_time, repeat_options, repeat_value, repeat_unit, repeat_end_date, repeat_end_time], [df])
        
demo.launch(debug=True, share=True)