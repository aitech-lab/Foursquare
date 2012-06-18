#pragma once

#include "ofMain.h"

class testApp : public ofBaseApp{

	public:
		void setup();
		void update();
		void draw();

		void keyPressed  (int key);
		void keyReleased(int key);
		void mouseMoved(int x, int y );
		void mouseDragged(int x, int y, int button);
		void mousePressed(int x, int y, int button);
		void mouseReleased(int x, int y, int button);
		void windowResized(int w, int h);
		void dragEvent(ofDragInfo dragInfo);
		void gotMessage(ofMessage msg);

		struct Checkin {
			unsigned int timestamp;
			double       lat;
			double       lng;
		};

		struct checkin_less {
			bool operator ()(Checkin const& a, Checkin const& b) const {
				if (a.timestamp < b.timestamp) return true;
				if (a.timestamp > b.timestamp) return false;
				return false;
			}
		};

		vector<Checkin> checkins;

		ofRectangle cityArea;
		unsigned int minTimestamp;
		unsigned int maxTimestamp;

		
};
