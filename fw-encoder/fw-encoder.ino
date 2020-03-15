/*
	SPI Encoder Monitor
	Thomas Ales, Coherent Photon Imaging, LLC
	March 2020

	Version 0.1

	For use with:
	Microchip ATmega2560 MCU - https://www.microchip.com/wwwproducts/en/ATmega2560

	Design Purpose:
	SPI-EM is designed to monitor the encoders on the Knife-edge detector. This
	does include the wrap-around logic for the 360* absolute encoder. The
	firmware is meant to be used in conjunction with the "Servocontroller" software.
	By itself, SPI-EM sends a serial update in the format of:
	NNN.NN,NNN.NN,NNN.NN,NNN.NN,NNN.NN,NNN.NN,NNN.NN,NNN.NN,NNN.NN,M
	Where NNN.NN is a float representing current angular position, and
			   M is an integer representing the total number of turns from the
			   arbitrary home position.
*/

#include <MLX90316.h>;

/* Physical Configuration for Encoders */

const int BLOCK1_SS[] = { A4, A5 };
const int BLOCK1_MISO = 25;
const int BLOCK1_SCLK = 24;

const int BLOCK2_SS[] = { A6, A7 };
const int BLOCK2_MISO = 22;
const int BLOCK2_SCLK = 23;

const int BLOCK3_SS[] = { A8, A9 };
const int BLOCK3_MISO = 28;
const int BLOCK3_SCLK = 29;

const int BLOCK4_SS[] = { A11, A12 };
const int BLOCK4_MISO = 27;
const int BLOCK4_SCLK = 27;

const int BLOCK5_SS = A10;
const int BLOCK5_MISO = 31;
const int BLOCK5_SCLK = 30;

volatile float CURRENT_ANGLE[9];
volatile int NUM_OF_TURNS[9];

MLX90316 BLOCK1_EN[2];
MLX90316 BLOCK2_EN[2];
MLX90316 BLOCK3_EN[2];
MLX90316 BLOCK4_EN[2];
MLX90316 BLOCK5_EN;

// Polling time in milliseconds
long POLLING_INTERVAL = 500;
long LAST_MS = 0;

/*	setup() - First function ran when MCU boots up.
*/
void setup()
{
	// Initalize Serial Connection
	// 115200 Baud, No Parity or Flow-Control
	Serial.begin(115200);

	// Set pin modes
	pinMode(BLOCK1_MISO, OUTPUT); (BLOCK1_SCLK, OUTPUT);
	pinMode(BLOCK2_MISO, OUTPUT); (BLOCK2_SCLK, OUTPUT);
	pinMode(BLOCK3_MISO, OUTPUT); (BLOCK3_SCLK, OUTPUT);
	pinMode(BLOCK4_MISO, OUTPUT); (BLOCK4_SCLK, OUTPUT);
	pinMode(BLOCK5_MISO, OUTPUT); (BLOCK5_SCLK, OUTPUT);

	// Initalize Encoder Objects
	for (int i = 0; i < 2; i++) {
		BLOCK1_EN[i].attach(BLOCK1_SS[i], BLOCK1_SCLK, BLOCK1_MISO);
		BLOCK2_EN[i].attach(BLOCK2_SS[i], BLOCK2_SCLK, BLOCK2_MISO);
		BLOCK3_EN[i].attach(BLOCK3_SS[i], BLOCK3_SCLK, BLOCK3_MISO);
		BLOCK4_EN[i].attach(BLOCK4_SS[i], BLOCK4_SCLK, BLOCK4_MISO);
		// Special case for block 5.
		if (i == 0)
		{
			BLOCK1_EN[i].attach(BLOCK5_SS, BLOCK5_SCLK, BLOCK5_MISO);
		}
	}
	Serial.println("MOTINTOK.");
}


String read_angles(int _encoder_num = 255)
{
	String _encoder_state;
	// If encoder state is 255 (default), report the state of all 
	// encoders.
	if (_encoder_num = 255)
	{
		// Read all the encoders
		for (int k = 0; k < 9; k++)
		{
			for (int i = 0; i < 2; i++)
			{
				CURRENT_ANGLE[k] = BLOCK1_EN[i].readAngle();
				k++;
				CURRENT_ANGLE[k] = BLOCK2_EN[i].readAngle();
				k++;
				CURRENT_ANGLE[k] = BLOCK3_EN[i].readAngle();
				k++;
				CURRENT_ANGLE[k] = BLOCK4_EN[i].readAngle();
				// Special case for block 5 encoders
				if (i == 0)
				{
					k++;
					CURRENT_ANGLE[k] = BLOCK5_EN.readAngle();
				}
			}
		}
		// Assemble the output string for the serial line
		for (int i = 0; i < 9; i++)
		{
			_encoder_state += String(CURRENT_ANGLE[i]) + String(",");
		}
		_encoder_state += "\n";
	}
	else {
		// TODO: Encoder specific polling request.
	}
	return _encoder_state;
}

/* loop() - Main function MCU loops infinitely in.
*/
void loop()
{
	delay(POLLING_INTERVAL);
	Serial.print(read_angles());
}