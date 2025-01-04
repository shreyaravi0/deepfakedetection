// Function to show the pop-up with explanation
function showPopup(type) {
    const popup = document.getElementById("popup");
    const popupTitle = document.getElementById("popup-title");
    const popupDescription = document.getElementById("popup-description");

    popup.style.display = "flex";  // Show the popup

    if (type === 'deepfake_face_swap') {
        popupTitle.innerText = "Face Swap Deepfake!";
        popupDescription.innerText = "This is a face swap deepfake, where the face of a person is digitally replaced with another person's face using AI technology. The deepfake can be convincing, but subtle signs like mismatched lighting or unnatural facial expressions often reveal it.";
    } else if (type === 'deepfake_audio') {
        popupTitle.innerText = "Audio Deepfake!";
        popupDescription.innerText = "Audio deepfakes use AI to replicate someone's voice, allowing them to say things they never actually said. Listen for unnatural pauses, weird intonations, or slight inconsistencies in tone, which may indicate an audio deepfake.";
    } else if (type === 'deepfake_video_manipulation') {
        popupTitle.innerText = "Video Manipulation Deepfake!";
        popupDescription.innerText = "This video has been manipulated to make it appear that someone is saying or doing something they didn't. Common signs of video manipulation include strange lighting, odd blinking patterns, or unnatural movements.";
    } else if (type === 'deepfake_avatar') {
        popupTitle.innerText = "Avatar Deepfake!";
        popupDescription.innerText = "This deepfake uses computer-generated avatars or virtual faces to create entirely fake people. These avatars can appear lifelike, but they often have issues with eye movement or skin texture that reveal their artificial nature.";
    } else if (type === 'deepfake_puppet') {
        popupTitle.innerText = "Puppet Deepfake!";
        popupDescription.innerText = "In this type of deepfake, the person’s face is replaced by a puppet-like figure. This is often used for comedic purposes but can be quite misleading when used in the wrong context.";
    } else {
        popupTitle.innerText = "Unknown Deepfake Type!";
        popupDescription.innerText = "This is an unknown deepfake type. You might be seeing a form of manipulation that doesn't match a traditional category.";
    }
}

// Function to close the pop-up
function closePopup() {
    const popup = document.getElementById("popup");
    popup.style.display = "none";  // Hide the popup
}
