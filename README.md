# AI Virtual Painter 

An interactive drawing application that uses **Computer Vision** to allow users to draw in the air using their fingers.

## Features
- **Red & Green Brushes:** Draw with different colors by selecting them from the top menu. 
- **Eraser Mode:** Clean your canvas using the dedicated eraser tool.
- **Smart Hand Tracking:** Uses **MediaPipe** to detect hand landmarks and distinguish between drawing and selection modes.

##  How It Works
1. **Selection Mode:** Raise both your index and middle fingers to move the cursor or select a color/eraser from the top menu.
2. **Drawing Mode:** Raise only your index finger to start drawing on the screen. 

##  Installation & Usage
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
