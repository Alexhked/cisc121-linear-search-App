import gradio as gr 
import random 
import time

#Function to create HTML boxes for list elements with color coding
def make_box_html(elements, highlight_index=None, found_index=None, not_found=False):
    """ provide elements in the list a colored box
    - highlight_index currently checing element (use yellow)
    - found_index element found (use green)
    - not_found when the element is not found (use red for all)
    - display -1 in red if element not found in the list
    """
    html = "<div style='display:flex; flex-wrap:wrap; gap:12px; margin:0;'>"
    for i, x in enumerate(elements):
        color = "white"
        border = "2px solid black"

        #Current checking element
        if highlight_index == i:
            color = "#FFD700"  # Yellow
            border = "2px solid white"
        #Found element
        if found_index == i:
            color = "#90EE90"  # Light Green
            border = "2px solid green"
        #Build HTML box 
        html += f"""
        <div style='
            width: 50px;height:50px;
            display:flex;justify-content:center;align-items:center;
            border:{border};border-radius:6px;
            font-size:20px;font-wight:bold;
            background-color:{color};
            margin:0;
        '>{x}</div>
        """
    html += "</div>"
    #If not found, add -1 box
    if not_found:
        html+= "<div style='margin-top:10px; color:red; font-weight:bold;'>return -1: Element not found</div>"
    return html

#Pesedocode highlighting function#
def highlight_code_line(line_num, failed = False, found = False):
    """
    highlight a specific line in the linear search pseduocode. 
    - failed = True ---> red (condition failed)
    - found = True ---> green (element found)
    - otherwise ---> yellow (current active line)
    """
    lines = [
        "def linear_search(elements, target):", #0
        "    i = 0",                           #1
        "    while i < len(elements):",        #2
        "        if elements[i] == target:",   #3
        "            return i",                #4
        "        else:",                       #5
        "            i+=1",                    #6
        "    return -1"                        #7
    ]
    html = "<pre style= 'font-size:16px; margin:0;'>"
    for idx, line in enumerate(lines):
        style = ""
        if idx == line_num:
            if failed:
                style = "background-color:red; color: white"
            elif found:
                style = "background-color: green; color: white"
            else:
                style = "background-color: yellow"
            html += f"<span style='{style}'>{line}</span>\n"
        else:
            html += line + "\n"
    html += "</pre>"
    return html
#Linear Search with step by step visualization#
def linear_search_animation(target,elements):
    """
    Generator function to animate linear search algorithm step by step.
    Highlights:
        - Yellow for current check
        - Red if condtion failed 
        - Green if element is found
    Yeilds HTML for array and pseduocode with steps description.
    """
    step_Text = ""
    try:
        target  = int(target)
    except ValueError:
        yield make_box_html(elements), "<p style='color:red'>Invalid input!</p>", ""
        return
    if target < -100 or target > 100:
        yield make_box_html(elements), "<p style='color:red'>Target out of range!</p>", ""
        return 
    i = 0
    while i < len(elements):
        #if element found, the highlight part is influenced by the help of AI 
        if elements[i] == target:
            #highlights if element[i] == target in green
            html_array = make_box_html(elements, highlight_index=i, found_index = i)
            code_html = highlight_code_line(3, found = True)
            step_Text += f"Step {i+1}: Found Target {target} at index {i}.<br>"
            yield html_array, code_html, f"<div style='font-size:20px !important;'>{step_Text}</div>"
            
            #highlight 'return i" in green 
            code_html = highlight_code_line(4, found = True)
            step_Text += f"Step {i+1}: Returning index {i}.<br>"
            yield html_array, code_html, f"<div style='font-size:20px !important;'>{step_Text}</div>"
            return 
        else: 
            #if element does not match target, yellow highlight
            html_array = make_box_html(elements, highlight_index=i)
            code_html =highlight_code_line(3, failed = True)
            step_Text += f"Step {i+1}:{elements[i]} != {target}, so increment i and continue.<br>"
            yield html_array, code_html, f"<div style='font-size:20px !important;'>{step_Text}</div>" 
            time.sleep(.5)

            #highlight "i+=1 line"
            code_html = highlight_code_line(6)
            step_Text += f"Step{i+1}: Increment i to {i+1}.<br>"
            yield html_array, code_html, f"<div style='font-size:20px !important;'>{step_Text}</div>"
            time.sleep(.5)
            i+=1
    #If element not found in the list, return -1 
    html_array = make_box_html(elements, not_found=True)
    code_html = highlight_code_line(7, failed = True)
    step_Text += f"Step {i+1} not found, Reurning False. <br>"
    yield html_array, code_html, f"<div style='font-size:20px !important;'>{step_Text}</div>"

#function to generate random list of numbers
def generate_List(num_items):
    elements = random.choices(range(-100,100),k = num_items) # made the range -100 to 100 for more variety for errors
    return elements, make_box_html(elements)

#Gradio Interface
with gr.Blocks() as demo: #heavily influenced by AI
    gr.HTML("""
<style>
/* FORCE ONLY BACKGROUNDS TO BE WHITE — DO NOT CHANGE TEXT COLOR */
:root, html, body, .gradio-container {
    --background-fill-primary: white !important;
    --background-fill-secondary: white !important;
    --background-fill-tertiary: white !important;

    /* keep text readable */
    --color-foreground: black !important;
    --color-background: white !important;

    --block-background-fill: white !important;
    --block-border-color: black !important;

    --input-background-fill: white !important;
    --input-border-color: black !important;
}

/* FIX: Ensure default text stays black */
* {
    color: black !important;
}

/* White backgrounds for containers and inputs */
.gr-box, .gr-panel, .gr-group, .gr-block, textarea, input, .gr-textbox {
    background: white !important;
    border: 2px solid black !important;
}

/* Remove dark mode behavior entirely */
.dark, [data-theme="dark"] {
    background: white !important;
    color: black !important;
}
</style>
""")

    #inputs controls, buttons and textboxes
    gr.Markdown("## Linear Search Algorithm")
    slider = gr.Slider(0,70,step=1,label="Number of items to generate")
    generate_btn = gr.Button("Generate")
    user_input = gr.Textbox(label="Enter the target Value (-100 to 100)")
    search_btn = gr.Button("Run Search")

    #layout for left side and right side, code display: left side displays List and right side displays code and steps
    with gr.Row():
        with gr.Column(elem_classes="boxed"):
            gr.Markdown("### Generated List")
            list_display = gr.HTML()

        with gr.Column(elem_classes="boxed"):
            gr.Markdown("### Linear Search Code")
            code_md = gr.HTML("code will appear here:")

    step_display = gr.Markdown("steps will appear here:")
    hidden_list = gr.State([])
    
    #Generate a new list
    generate_btn.click(
        fn=generate_List,
        inputs = [slider],
        outputs = [hidden_list, list_display]
    )
    # Runs linear search animation
    search_btn.click(
        fn = linear_search_animation,
        inputs = [user_input, hidden_list],
        outputs = [list_display, code_md, step_display]
    )
    #Launch the Gradio App automatically in browser.
demo.launch(share=False, inbrowser=True)