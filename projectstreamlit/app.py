import streamlit as st
import requests
import json
import sqlite3
import os
from PIL import Image

# Initialize SQLite Database
DB_FILE = "deepfake_db.sqlite"
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def init_db():
    """Initialize the SQLite database."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS deepfakes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                label TEXT
            )
        """)
init_db()

# Helper function to save reported image to the database
def save_to_db(filename, label):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO deepfakes (filename, label) VALUES (?, ?)", (filename, label))

# Helper function to fetch reported images from the database
def fetch_reported_images():
    with sqlite3.connect(DB_FILE) as conn:
        return conn.execute("SELECT id, filename, label FROM deepfakes").fetchall()

# Streamlit UI
st.sidebar.title("Deepfake Detection")
page = st.sidebar.selectbox("Navigate", ["Home", "Report", "Education"])

# Home Page: Deepfake Detection
if page == "Home":
    st.title("Deepfake Detection with Sightengine")
    st.write("Upload an image to check if it's a deepfake.")

    # Input API credentials
    api_user = "1276713923"
    api_secret = "KTpUidym5XcbNg7nhBEeYGYy2rLeUaA3"

    # Upload image
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        try:
            # Save uploaded file temporarily
            with open(os.path.join(UPLOAD_FOLDER, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Send the file to Sightengine API
            with open(os.path.join(UPLOAD_FOLDER, uploaded_file.name), "rb") as img:
                files = {'media': img}
                params = {
                    'models': 'deepfake',
                    'api_user': api_user,
                    'api_secret': api_secret
                }
                response = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

            # Process response
            if response.status_code == 200:
                result = json.loads(response.text)
                st.subheader("Detection Results")
                st.json(result)

                # Allow reporting the deepfake
                if st.button("Report as Deepfake"):
                    save_to_db(uploaded_file.name, "ai")
                    st.success("Image reported as deepfake and saved to the database.")
            else:
                st.error("Error from API: " + response.text)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.write("Please upload an image.")

# Report Page: Display and Label Reported Images
elif page == "Report":
    st.title("Reported Deepfake Images")
    reported_images = fetch_reported_images()

    if reported_images:
        for image_id, filename, label in reported_images:
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.exists(image_path):
                st.image(Image.open(image_path), caption=f"ID: {image_id}, Label: {label}")
    else:
        st.write("No reported images yet.")

elif page == "Education":
    st.title("Understanding Deepfakes")
    st.markdown("""
    ## What are Deepfakes?

    **Deepfakes** are synthetic media created using advanced artificial intelligence (AI) techniques that can manipulate or generate visual and audio content, making it appear highly realistic. These deepfakes often imitate or replace the likeness of one person with another, in images, videos, or audio recordings. The term ‘deepfake’ derives from two concepts: **Deep Learning** (a subset of machine learning) and **Fake** (altered or manipulated content). As the technology continues to improve, the distinction between authentic and manipulated content becomes harder to detect by the human eye.

    The technology behind deepfakes is based on **Generative Adversarial Networks (GANs)**, a class of machine learning algorithms that use two neural networks: a generator and a discriminator. The generator creates synthetic media, while the discriminator attempts to distinguish between real and fake data. Through a feedback loop, both networks evolve and improve over time, leading to increasingly convincing results.

    While deepfake technology can be used creatively in movies and art, it is also being weaponized for malicious purposes, such as spreading misinformation, defaming individuals, and committing fraud.

    ## How Are Deepfakes Created?

    Deepfakes are typically generated using advanced **machine learning algorithms**, specifically **Generative Adversarial Networks (GANs)**. The process involves the following steps:

    1. **Training Data Collection**: Large datasets of real media (images, videos, or audio) are gathered. For video deepfakes, the dataset often includes multiple angles of a person’s face, voice samples, and different lighting conditions to capture as much of the subject’s features as possible.
    
    2. **Preprocessing**: The raw data is preprocessed to normalize lighting, resize images, and align facial features in a consistent way. This step makes it easier for the AI to learn the features of the person’s face or voice.

    3. **Training the Generator**: The **generator** learns to produce synthetic images or videos that resemble the target subject. Over time, it produces media that becomes progressively harder to distinguish from real footage.

    4. **Training the Discriminator**: The **discriminator** is responsible for distinguishing between real and fake data. It provides feedback to the generator, telling it how well or poorly the content aligns with the real data.

    5. **Iterative Refinement**: The process continues with both the generator and discriminator learning from each other until the synthetic media appears highly realistic.

    ## Types of Deepfakes

    Deepfakes can take many forms, manipulating both visual and audio content. Here are the most common types:

    ### 1. **Face Swapping**
    - **Face swapping** is the most popular and widely recognized form of deepfake. It involves replacing one person’s face with another in a video or image, typically with the goal of deceiving viewers. While it can be fun and used for harmless entertainment (such as swapping faces between celebrities in films), it can also be used to spread misleading content. In malicious contexts, deepfake creators use this technique to make public figures appear to engage in criminal or inappropriate actions.

    ### 2. **Lip Syncing**
    - **Lip syncing** deepfakes manipulate the facial movements of an individual to make it appear as though they are speaking words that they never actually uttered. This is done by replacing or altering the movement of a person’s mouth to match the audio track of another speech or voice recording. The technology has reached a point where the lips move so convincingly that the fake nature of the video can only be detected by the most advanced algorithms.

    ### 3. **Voice Cloning**
    - **Voice cloning** is the process by which AI mimics the voice of an individual. A small sample of the person’s voice is enough for a machine learning algorithm to replicate their tone, accent, cadence, and even their speech patterns. This type of deepfake can be used in scenarios like creating fraudulent phone calls or producing fake audio recordings of celebrities, political leaders, or even family members for malicious purposes.

    ### 4. **Full-body Animation**
    - This type of deepfake creates a synthetic body, often based on a 3D model of a person, to perform actions that the real person never performed. These full-body deepfakes can be used in movies for special effects, but they also pose significant risks, especially when used to create fake videos of individuals engaging in harmful or illegal activities.

    ### 5. **Audio Deepfakes**
    - **Audio deepfakes** are manipulated or artificially generated audio clips that replicate a person’s speech, tone, and cadence. These are often used for fraudulent activities, such as making it sound like someone is speaking to authorize financial transactions or make defamatory statements. This type of deepfake is especially concerning in the context of corporate fraud, where attackers impersonate CEOs or senior executives.

    ## How to Detect Deepfakes

    As deepfake technology improves, detecting manipulated media becomes increasingly challenging. However, there are several methods and tools being developed to identify inconsistencies and signs of manipulation.

    ### 1. **Inconsistent Lighting**
    - One of the most common giveaways of a deepfake is inconsistent lighting. The lighting on a deepfake’s face or body might not align properly with the background or the light source, creating noticeable mismatches. Shadows, highlights, and reflections may appear unnatural or even completely absent, especially in videos that involve dynamic lighting conditions.

    ### 2. **Unnatural Facial Movements**
    - Even the most advanced deepfakes struggle to replicate the full range of natural human facial movements. For example, AI-generated faces may have a stiff or robotic smile, or they might blink unnaturally. Sometimes, deepfakes fail to properly simulate the way a person’s face moves when they speak, creating an unsettling effect.

    ### 3. **Texture Irregularities**
    - Deepfake videos often exhibit texture issues, especially around areas like hair, teeth, or skin. These textures can appear blurry or unnaturally smooth, making it obvious that the content has been altered. A well-crafted deepfake can hide these issues, but under close scrutiny, they are still present.

    ### 4. **Audio-Visual Inconsistencies**
    - In the case of voice and lip-syncing deepfakes, the alignment between the person’s lip movements and the audio may be off. For instance, a person’s mouth may move in ways that don’t correspond with the words being spoken. Similarly, audio deepfakes may contain odd pauses or unnatural speech patterns that sound different from the individual’s normal tone.

    ### 5. **Eye Movement and Blink Patterns**
    - AI-generated deepfakes often fail to capture the natural rhythm of eye movements and blinking. Real human eyes exhibit a random blinking pattern, and slight involuntary movements occur when someone speaks or interacts with their environment. Deepfakes may have unnatural, robotic blinks or fail to blink altogether.

    ## Ethical Concerns

    While deepfakes can be entertaining and even useful in creative industries, they also present significant ethical dilemmas. Here are some of the key concerns:

    ### 1. **Spread of Misinformation**
    - Deepfakes have become a tool for spreading **misinformation** and **fake news**. Fake videos of politicians, celebrities, or public figures saying or doing things they never did can easily go viral, potentially leading to misinformation campaigns or political unrest.

    ### 2. **Privacy Violations**
    - One of the most concerning ethical issues is the violation of **privacy**. Deepfakes allow malicious actors to create videos or audio recordings of individuals without their consent, often leading to the creation of explicit or harmful content. This undermines personal privacy and can cause emotional, financial, or reputational harm.

    ### 3. **Manipulation of Public Opinion**
    - Deepfakes can be weaponized to manipulate **public opinion**. By creating convincing fake videos or audio clips of public figures engaging in scandalous or illegal behavior, malicious actors can influence elections, defame individuals, or destabilize political systems.

    ### 4. **Psychological Impact**
    - The ability to create convincing fake content has a profound **psychological impact**. Individuals who are targeted by deepfakes may experience emotional distress, anxiety, and loss of trust in the media. This can lead to widespread skepticism, where people no longer know what content is authentic, potentially leading to a collapse in societal trust.

    ### 5. **Defamation and Reputation Damage**
    - Public figures, such as politicians, celebrities, and business leaders, are at risk of **reputation damage** from deepfakes. These fake videos can create false impressions, ruin careers, or destroy relationships. Even private individuals can become targets of malicious deepfakes, facing harassment or defamation.

    ## Future Directions and Solutions

    As deepfakes continue to evolve, so do the efforts to counter their negative impact. Several initiatives and technologies are being developed to address the challenges posed by deepfakes:

    ### 1. **AI-Powered Detection Tools**
    - There is a growing effort to develop **AI-powered deepfake detection tools**. These tools use machine learning algorithms trained to identify inconsistencies in videos, audio, and images. By analyzing the content for artifacts, irregularities, or inconsistencies, these tools can help flag suspicious media and prevent its spread.

    ### 2. **Legislation and Regulation**
    - Governments are increasingly focusing on **legislation and regulation** to address the misuse of deepfakes. Countries like the United States and the European Union have proposed laws that criminalize the creation and distribution of malicious deepfakes. Legal frameworks are being designed to hold offenders accountable and provide justice to victims.

    ### 3. **Public Awareness and Education**
    - Public awareness campaigns and **education** are key to combating the spread of deepfakes. By educating the public on how to recognize deepfakes, the dangers they pose, and how to report them, we can reduce the potential harm. Schools, businesses, and organizations are all integrating media literacy programs that include training on recognizing manipulated content.

    ### 4. **Transparency and Accountability**
    - Platforms like social media, video-sharing sites, and news outlets are being urged to implement more **transparency** in the content they distribute. By using tools like **watermarking**, digital signatures, or blockchain, content creators can prove the authenticity of media. This ensures that viewers can verify whether a video or image is legitimate.

    ## Conclusion

    Deepfakes are an exciting yet concerning development in the field of artificial intelligence. They have the potential to revolutionize entertainment, art, and content creation, but also pose significant threats to privacy, security, and trust. As this technology continues to evolve, it is crucial for society to balance innovation with ethical considerations, focusing on solutions that minimize harm while encouraging responsible use.

    With continued research, education, and regulation, we can ensure that deepfakes are used for good and their risks are effectively managed.
    """)


