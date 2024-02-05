import gradio as gr
import google.generativeai as google_key
from history import DatabaseHandler


'''What is Gradio - Interface is Gradio's main high-level class, and 
allows you to create a web-based GUI / demo around a machine learning model (or any Python function) in a 
few lines of code.'''

db_handler = DatabaseHandler()

google_key.configure(api_key='AIzaSyDoY1gTJWLHkS61QAt7ygpF5qQdixANR2Q')
 

def generate_code(prompt):
    try:
        models = [m for m in google_key.list_models() if 'generateText' in m.supported_generation_methods]
       
        model = models[0].name if models else None
        if model:
            completion = google_key.generate_text(
                model=model,
                prompt=prompt,
                temperature=0,
                max_output_tokens=200,
            )
            response = completion.result
            db_handler.insert_data(prompt, response)
            return response
        
    except Exception as e:
        return f"Error: {e}"


def show_history():
    
    history_data = db_handler.fetch_all_data()
    data= "\n".join([f"Input: {entry['input']}\nOutput: {entry['output']}\n{'-'*50}" for entry in history_data])
    return data


css = """
#warning {background-color: #FFCCCB}

"""

with gr.Blocks(css=css) as demo:
    with gr.Row():
        with gr.Column(scale=25):
            title = gr.HTML("""
                <div style="background-color: #FFCCCB; padding: 10px; text-align: center; border-radius: 10px;">
                    <strong style="font-size: 24px;">History</strong>
                </div>
            """)
            his_out = gr.TextArea(lines=21,elem_id="warning")
            btn_show_history = gr.Button("Show History")
            
            btn_show_history.click(fn=show_history, outputs=his_out)
                 
        with gr.Column(scale=75):
            title = gr.HTML("""
                <div style="background-color: #e6e6e6; padding: 10px; text-align: center; border-radius: 10px;">
                    <strong style="font-size: 24px;">CodeGen App</strong>
                </div>
            """)
                                                                                      
         
            out = gr.TextArea(lines=15)
            inp = gr.Textbox(placeholder="What do you want to search here?")
            btn_run = gr.Button("Run")
            btn_run.click(fn=generate_code, inputs=inp, outputs=out)
           
demo.launch(share=True)