import streamlit as st
from story_generator import generate_story_from_images,narrate_story
from PIL import Image

st.title("AI STORY GENERATOR from Image")

st.markdown("Upload **1 to 10** images , choose a style and AI will narate a story for you !")

with st.sidebar:
    st.header("Controls : ")
    
    # File upload

    uploaded_files = st.file_uploader(
        "Upload your images : ",
        type=["jpeg","png","jpg"],
        accept_multiple_files = True,


    )
    #  Select box 
    story_style = st.selectbox(
        'Choose a story style : ',
        ('Comedy', 'Horror', 'Adventure','Fairy Tale','Morale','Mystery','Thriller')
        
        )
    
    generate_button = st.button("Generate Story and Narration",type="primary")

    # Main logic

if generate_button:
    if not uploaded_files:
        st.warning("Please upload atleast 1 image.",icon="⚠️")

    elif len(uploaded_files)>10:
        st.warning("Please upload max of 10 images.",icon="⚠️")

    else:
        with st.spinner("AI is narrating your story...... This may take few moments.") :
            try:
                pil_Images = [Image.open(uploaded_file) for uploaded_file in uploaded_files]    
                st.subheader("Your Visual Inspiration :")
                image_columns = st.columns(len(pil_Images))

                for i,image in enumerate(pil_Images):
                    with image_columns[i] :
                        st.image(image,width="stretch")

                generate_story  =  generate_story_from_images(pil_Images,story_style)

                if "Error" in generate_story or "failed" in generate_story or "API key" in generate_story:
                    st.error(generate_story)

                else:
                    st.subheader(f"Your {story_style} Story : ")
                    st.success(generate_story) 

                st.subheader("Listen to story : ")
                audio_file = narrate_story(generate_story)
                if audio_file:
                    st.audio(audio_file,format="audio/mp3")


            except Exception as e:
                st.error(f"An application error occured : {e}")





    


    
    
    
    


