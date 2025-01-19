import pywhatkit as kit

# Specify the phone number (with country code) and the message
phone_number = "+919651648985"
message = "Hello from Miran! Check out this video: "

# Send the message instantly


def send_whatsapp_message():
    kit.sendwhatmsg_instantly(
        phone_number,
        caption=message + "https://www.youtube.com/shorts/3S7Ub_gQm5c",
    )
