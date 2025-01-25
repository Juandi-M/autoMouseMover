import customtkinter
import os
from PIL import Image

class TestApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Basic window setup
        self.title("Button Test")
        self.geometry("300x200")

        # Load image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.us_flag = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "us_flag.png")),
            size=(40, 40)
        )

        # Create button
        self.button = customtkinter.CTkButton(
            self,
            text="",
            image=self.us_flag,
            width=60,
            height=60,
            corner_radius=70,
            fg_color="#1A1A27",
            hover_color="#7E6BE8"
        )
        self.button.place(relx=0.5, rely=0.5, anchor="center")

if __name__ == "__main__":
    app = TestApp()
    app.mainloop()