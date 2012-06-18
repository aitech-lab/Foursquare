#include "testApp.h"
#include <stdio.h>

//--------------------------------------------------------------
void testApp::setup(){
	
	ofFile   csvf = ofFile("test-data.csv");
	ofBuffer csvb = csvf.readToBuffer();
	minTimestamp = INT_MAX*2;
	maxTimestamp = 0;

	while(!csvb.isLastLine()) {
		string line = csvb.getNextLine();
		vector<string> items = ofSplitString(line, ",");
		Checkin checkin; 
		checkin.timestamp = ofToInt  (items.at(0)); 
		checkin.lng       = ofToFloat(items.at(1));
		checkin.lat       = ofToFloat(items.at(2));
		checkins.push_back(checkin);

		if(minTimestamp > checkin.timestamp) minTimestamp = checkin.timestamp;
		if(maxTimestamp < checkin.timestamp) maxTimestamp = checkin.timestamp;

	}
	csvf.close();
	
	sort(checkins.begin(), checkins.end(), checkin_less());

	
	// # MOSCOW BOUNDS
	cityArea.x      = 37.33204993;
	cityArea.y      = 55.55701887;
	cityArea.width  = 37.89647254 - cityArea.x; 
	cityArea.height = 55.92578046 - cityArea.y;

	ofBackground(0);

}

//--------------------------------------------------------------
void testApp::update(){

}

//--------------------------------------------------------------
void testApp::draw(){
	
	float sw = ofGetWidth ();
	float sh = ofGetHeight();
	float mx = ofGetMouseX();

	float timescale   = (float) (maxTimestamp - minTimestamp) / sw;
	float widthscale  = (float) cityArea.width  / sw;
	float heightscale = (float) cityArea.height / sh;
	float mt          =  mx * timescale;
	
	ofPath p;
	p.setFilled(false);
	ofEnableAlphaBlending();

	for(int i=0; i<checkins.size(); i++) {
		Checkin& checkin = checkins.at(i);
		int x = (checkin.lat-cityArea.x)/widthscale  ;
		int y = sh-(checkin.lng-cityArea.y)/heightscale;
		
		int tx = (float) (checkin.timestamp-minTimestamp) / timescale;
		float x2 = (tx-mx)*(tx-mx);
		float dt = exp(-x2/4000.0);
		float dx = exp(-x2/8000.0);

		ofColor c(0x40 + 0xC0*dt, 0x80 + 0x7F*dx, 0xFF - 0xC0*dt, 0x00 + 0xFF*dx); 
		
		ofSetColor(c);
		ofCircle(x, y, 3+25*dt);

		if (dx > 0.95) {
			p.setColor(c);
			p.curveTo(x,y);
		}
		
		if (dx >= 0.95) {
			time_t ts = checkin.timestamp;
			ofDrawBitmapString(ctime(&ts), x, y);
		}
		ofNoFill();
		
		c.a = 255;
		ofSetColor(c);
		ofLine(x-5, y  , x+4, y  );
		ofLine(x  , y-4, x  , y+5);
		ofLine(tx+dx*(tx-mx), sh, tx+dx*(tx-mx), sh-20-30*dt);
		
	}
	
	p.draw();

	ofSetColor(0xFF, 0xFF, 0xFF, 0x80);
	time_t t = mt + minTimestamp;
	ofLine(mx, sh, mx, sh-70);
	ofSetColor(255);
	ofDrawBitmapString(ctime(&t), mx, sh-60);
}

//--------------------------------------------------------------
void testApp::keyPressed(int key){

}

//--------------------------------------------------------------
void testApp::keyReleased(int key){

}

//--------------------------------------------------------------
void testApp::mouseMoved(int x, int y ){

}

//--------------------------------------------------------------
void testApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void testApp::mousePressed(int x, int y, int button){

}

//--------------------------------------------------------------
void testApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void testApp::windowResized(int w, int h){

}

//--------------------------------------------------------------
void testApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void testApp::dragEvent(ofDragInfo dragInfo){ 

}