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

	vector<ofPoint> pathPoints;
	for(int i=0; i<checkins.size(); i++) {
		Checkin& checkin = checkins.at(i);
		int x = (checkin.lat-cityArea.x)/widthscale  ;
		int y = (checkin.lng-cityArea.y)/heightscale;
		pathPoints.push_back(ofPoint(x,y));
		
		int tx = (float) (checkin.timestamp-minTimestamp) / timescale;
		ofLine(tx, sh, tx, sh-20);
		ofLine(x-5, y  , x+5, y  );
		ofLine(x  , y-5, x  , y+5);
	}

	ofEnableAlphaBlending();
	ofSetHexColor(0x7FFFFFFF);
	ofPolyline path(pathPoints);
	path.draw();

	ofLine(mx, sh, mx, sh-40);
	ofDrawBitmapString(ofToString((int)mt), mx, sh-30);
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