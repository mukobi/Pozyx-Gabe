import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import oscP5.*; 
import org.gwoptics.graphics.graph2D.Graph2D; 
import org.gwoptics.graphics.graph2D.traces.*; 
import org.gwoptics.graphics.graph2D.backgrounds.*; 
import org.gwoptics.graphics.GWColour; 
import processing.serial.*; 
import java.lang.Math.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class pozyx_orientation3D_PSU extends PApplet {









boolean serial = false;           // set to true to use Serial(Arduino), false to use OSC messages (Python).

int oscPort = 8888;               // change this to your UDP port
String serialPort = "COM13";      // change this to your COM port 


/////////////////////////////////////////////////////////////
//////////////////////  variables //////////////////////////
/////////////////////////////////////////////////////////////

OscP5 oscP5;
Serial myPort;

int     lf = 10;       //ASCII linefeed
String  inString;      //String for testing serial communication
int[] rgb_color = {0, 0, 255, 0, 160, 122, 0, 255, 0, 255}; // color array for graph traces

Graph2D g_acc, g_gyro, g_mag; // objects to hold the 3 graphs
PImage compass_img; // compass image
PImage psu_logo; // psu logo image

/////////////////////////////////////////////////////////////
///////////// sensordata variables //////////////////////////
/////////////////////////////////////////////////////////////

// this section just initializes all of the variables to hold the sensor data
float x_angle = 0;  
float y_angle = 0;
float z_angle = 0;

float speed_x = 0;
float speed_y = 0;
float speed_z = 0;

float lin_acc_x = 0;
float lin_acc_y = 0;
float lin_acc_z = 0;

float quat_w, quat_x, quat_y, quat_z;
float grav_x, grav_y, grav_z;
float heading = 0;
float pressure = 0;

String calib_status = "";

// array of sensor data over multiple timesteps
// These hold all the data recorded by each sensor which is then accessed
// by the graphs to draw the traces
ArrayList<rangeData> accData;
ArrayList<rangeData> magData;
ArrayList<rangeData> gyroData;
 
 
/////////////////////////////////////////////////////////////
///////// class needed for the timeseries graph /////////////
/////////////////////////////////////////////////////////////

// class representing each data point for each trace of each graph
// implements the ILine2DEquation interface so the Graph2D objects
// can call computePoint and graph the data
class rangeData implements ILine2DEquation{ 
    private double curVal = 0; // current value

    public void setCurVal(double curVal) { 
      this.curVal = curVal;      
    }
    
    // this function never used in this sketch due to how computePoint works
    public double getCurVal() { 
      return this.curVal;
    }
    
    // method of ILine2DEquation that gets the Y value for each X value on the graph
    public double computePoint(double x,int pos) { 
      return curVal;
    }
}


//setup() is run only once when the program starts
public void setup(){
  // the size function sets window size and graph type
  // sets window size to 1100x800 px and enables Processing 3D graphs with P3D
  
  surface.setResizable(true); // allows the window to be resized
  //the stroke function sets the color used to draw lines and borders around shapes.
  //here, it sets all lines and borders after it to be black
  stroke(0,0,0);
  // colorMode clarifies that the numbers we just passed to stroke are RGB values from 0 to 255
  // (256 total possible) instead of things like hue, saturation, and brightness values
  colorMode(RGB, 256); 
  
   psu_logo = loadImage("psu_logo.png");
    
  compass_img = loadImage("compass.png"); // loads Processing Image (PImage) variable for compass
 
  //establishes connection for either serial or osc
  if(serial){
    try{
      myPort = new Serial(this, serialPort, 115200);
      myPort.clear();
      myPort.bufferUntil(lf);
    }catch(Exception e){
      println("Cannot open serial port.");
    }
  }else{
    try{
      oscP5 = new OscP5(this, oscPort);
    }catch(Exception e){
      println("Cannot open UDP port");
    }
  }
  
       
  // initialize running traces
  // each of these Graph2Ds are set with this program as the parent (this),
  // width 400px (400), height 200px (200), and crossAxesAtZero false (false) 
  // which makes the X and Y axes not have to meet at (0,0)
  g_acc = new Graph2D(this, 400, 200, false); 
  g_mag = new Graph2D(this, 400, 200, false);
  g_gyro = new Graph2D(this, 400, 200, false);   
  
  // initialize the three graph data variables as new arrays of rangeData objects
  accData = new ArrayList<rangeData>();
  magData = new ArrayList<rangeData>();
  gyroData = new ArrayList<rangeData>();    
  
  //for each of the three different colors of lines on each graph
  for(int i=0; i<3; i++){
    //create a new rangeData data value to be used for acceleration graph
    rangeData r = new rangeData();
    //start off dataset with an unset rangeData to allow later adding of data
    accData.add(r);
    // RollingLine2DTrace allows for a graph to constantly scroll left, like a seismometer
    // making this a RollingLine2DTrace is also the reason why the X axes of the graphs scroll
    // constructor take an equation to graph (r), a graph refresh rate in ms (100), 
    // and an x increment specifying how much the X value increases each update. Since we want
    // x to be in seconds and the graph updates 10 times per second, xIncr is 0.1
    RollingLine2DTrace rl = new RollingLine2DTrace(r ,100,0.1f);
    // by using the incrementing of i and the rgb_color array above, this sets the color
    // of each line on the graph to be different
    rl.setTraceColour(rgb_color[i%10], rgb_color[(i+1)%10], rgb_color[(i+2)%10]);
    // sets pixel width of each line
    rl.setLineWidth(2);
    // adds the line as a trace on the acceleration graph
    g_acc.addTrace(rl);
    
    
    //same as above, but for for magnetic data
    r = new rangeData();
    magData.add(r);
    rl = new RollingLine2DTrace(r ,100,0.1f);
    rl.setTraceColour(rgb_color[i%10], rgb_color[(i+1)%10], rgb_color[(i+2)%10]);
    rl.setLineWidth(2);      
    g_mag.addTrace(rl);
    
    //same as above, but for for gyro (angular velocity) data
    r = new rangeData();
    gyroData.add(r);
    rl = new RollingLine2DTrace(r ,100,0.1f);
    rl.setTraceColour(rgb_color[i%10], rgb_color[(i+1)%10], rgb_color[(i+2)%10]);
    rl.setLineWidth(2);      
    g_gyro.addTrace(rl);    
   
  }
  
  // create the accelerometer graph
  g_acc.setYAxisMin(-2.0f);        // minimum y axis value
  g_acc.setYAxisMax(2.0f);         // maximum y axis value
  g_acc.position.y = 50;           // distance from top of window
  g_acc.position.x = 100;          // distance from left of window
  g_acc.setYAxisTickSpacing(0.5f); // y axis tick mark label increments
  g_acc.setXAxisMax(5f);           // maximum x axis, effectively sets graph data width 
  g_acc.setXAxisLabel("time (s)"); // x axis label
  g_acc.setYAxisLabel("acceleration [g]"); // y axis label
  g_acc.setBackground(new SolidColourBackground(new GWColour(1f,1f,1f))); // sets white background
  
  // create the magnetometer graph
  //same as above, but for magnetic graph
  g_mag.setYAxisMin(-80.0f);
  g_mag.setYAxisMax(80.0f);
  g_mag.position.y = 300;
  g_mag.position.x = 100;    
  g_mag.setYAxisTickSpacing(40f);
  g_mag.setXAxisMax(5f);
  g_mag.setXAxisLabel("time (s)");
  g_mag.setYAxisLabel("magnetic field strength [\u00b5T]");
  g_mag.setBackground(new SolidColourBackground(new GWColour(1f,1f,1f)));
  
  // create the gyrometer graph
  //same as above, but for angular velocity graph
  g_gyro.setYAxisMin(-1000.0f);
  g_gyro.setYAxisMax(1000.0f);
  g_gyro.position.y = 550;
  g_gyro.position.x = 100;    
  g_gyro.setYAxisTickSpacing(250f);
  g_gyro.setXAxisMax(5f);
  g_gyro.setXAxisLabel("time (s)");
  g_gyro.setYAxisLabel("angular velocity [deg/s]");
  g_gyro.setBackground(new SolidColourBackground(new GWColour(1f,1f,1f)));
  
}

// draw() is run once every frame to draw the frame
public void draw(){
    background(106,127,16); // PSU Green
       
    // show some text
    // the fill function sets the color used to fill shapes
    // this sets everything below it to be filled in black
    fill(0,0,0);
    // adds calibration status text to bottom right
    text("Calibration status:", 550, 730);
    // adds the state of the calibration status below the previous line
    text(calib_status, 550, 750);   
    // adds pressure label text
    text("Pressure: " + pressure + "Pa", 550, 710);
       
    // draw the 3 graphs by calling internal methods to generate each part of the graphs   
    g_acc.draw();
    g_mag.draw();
    g_gyro.draw();
    
    //Show 3D orientation data
    // sets lines and borders make below this to be black
    stroke(0,0,0);
    // sets thin 0.01 stroke width
    strokeWeight(0.01f);
    
    ///////////////START 3D ORIENTATION MATRIX DISPLAY///////////////
    
    // Pushes the current transformation matrix onto the matrix stack.
    // Essentially, that means it marks the start of a new shape to draw (our 3D orientation box)
    pushMatrix();
    // translate(x,y,z) moves a shape in the window
    // translates the shape on the window to the bottom right
    // -50 in the z means 50px away from the screen, effectively shrinking the box a little
    // our drawing "cursor" is now at (800,500,-50) and we draw everthing after it relative
    // to that point. From how draw_rect() works, this is the center of the box
    translate(800, 500, -50);
    
    // initial 3D rotation of the box so that when the pozyx is flat, the box is too
    // rotateX means rotated about the x axis -pi/2 rad, and rotateZ over the z axis pi/2 rad
    rotateX(radians(-90));
    rotateZ(radians(90));
    // calls the quat_rotate function defined at the bottom of this sketch, which rotates
    // the box and red line based on the quaternion values read from the Pozyx
    quat_rotate(quat_w, quat_x, quat_y, quat_z);
    
    // draw the 3D box (the green box representing orientation)
    // calls draw_rect defined below, passing in integers representing its green color
    draw_rect(93, 175, 83);
    
    // draw lines
    //sets thicker 0.1px stroke weight for lines
    strokeWeight(0.1f);
    // makes a line from the center of the box down towards the gravitational pull
    // this is the black line on the bottom of the green box. Interesting is the use
    // of the gravity measurements from the Pozyx to make sure it always points "down"
    // instead of putting this outside of the orientation matrix and drawing it towards
    // what the window thinks is down
    line(0,0,0, grav_x*2, grav_y*2, grav_z*2);    
    // sets stroke color (lines and borders) to red
    stroke(200,0,0);
    // draws a line going from (0,0,0) to (0,0,1). Keep in mind that this is still within the
    // rotation matrix and thus relative to its rotate and quat_rotate calls. This is the 
    // little red line going below the green box
    line(0,0,0, 0, 0, 1);
    
    // end rotation
    // popMatrix pops the current transformation matrix off the matrix stack. In effect, this
    // means we are done working on the green box + black line + red line orientation matrix
    popMatrix();
    ///////////////END 3D ORIENTATION MATRIX DISPLAY///////////////
    
    
    // show the linear acceleration in body coordinates
    int x_center = 700, y_center = 150;
    // sets lines and borders to black
    stroke(0,0,0);
    // 1 pixel stroke weight
    strokeWeight(1);
    // makes the horizontal black line for body coordinates
    line(x_center-75, y_center, x_center+75, y_center);
    // makes the vertical black line for body coordinates
    line(x_center, y_center-75, x_center, y_center+75);
    // designate that the circles we will make will be positioned by their centers
    ellipseMode(CENTER);
    // create a static ellipse with width and height of 50px, thus making a circle
    ellipse(x_center, y_center, 50, 50);
    // create a dynamic ellipse that moves and resizes with linear acceleration
    ellipse(x_center+lin_acc_x/50, y_center-lin_acc_y/50, 50*(1-lin_acc_z/1000), 50*(1-lin_acc_z/1000));
    // set fill color to black
    fill(0,0,0);
    // add text labeling the linear acceleration circles
    text("Linear acceleration\n(body coordinates)", x_center-50, y_center + 100);
    
    // show the linear acceleration in world coordinates
    //same as above, just for world coordinates
    x_center = 900;
    fill(93, 175, 83);
    stroke(0,0,0);
    strokeWeight(1);
    line(x_center-75, y_center, x_center+75, y_center);
    line(x_center, y_center-75, x_center, y_center+75);
    ellipseMode(CENTER);
    ellipse(x_center, y_center, 50, 50);
    
    
    // this section uses vector math to convert body coordinates linear acceleration into world coordinates via rotation
    PVector lin_acc = new PVector(lin_acc_x, lin_acc_y, lin_acc_z);
    //PVector lin_acc = new PVector(grav_x*1000.0f, grav_y*1000.0f, grav_z*1000.0f);    // test to verify the rotation
    lin_acc = quaternion_rotate(quat_w, quat_x, quat_y, quat_z, lin_acc);
    lin_acc.y = -lin_acc.y;
    lin_acc.z = -lin_acc.z;
       
    
    ellipseMode(CENTER);
    ellipse(x_center+lin_acc.x/50, y_center-lin_acc.y/50, 50*(1-lin_acc.z/1000), 50*(1-lin_acc.z/1000));
    fill(0,0,0);
    text("Linear acceleration\n(world coordinates)", x_center-50, y_center + 100);
    /*    
    text("x: " + grav_x*1000.0f , 550, 310);
    text("y: " + grav_y*1000.0f , 550, 330);
    text("z: " + grav_z*1000.0f , 550, 350);
    
    text("x: " + lin_acc_x , 550, 310);
    text("y: " + lin_acc_y , 550, 330);
    text("z: " + lin_acc_z , 550, 350);
    
    text("x: " + lin_acc.x , 650, 310);
    text("y: " + lin_acc.y , 650, 330);
    text("z: " + lin_acc.z , 650, 350);
    */
    
    // draw the heading (compass)
    int img_size = 160;
    // creates a compass with center at (1000, 700)
    image(compass_img, 1000-img_size/2, 700-img_size/2, img_size, img_size);
    // change stroke color to red
    stroke(255,0,0);
    // 3 pixel stroke weight
    strokeWeight(3);
    // creates line from compass center (1000, 700) in the direction of Pozyx heading
    line(1000, 700, 1000+50*cos(radians(heading)), 700+50*sin(radians(heading))); 
    
    int img_width = 160;
    int img_height = 43;
    image(psu_logo, width - img_width - 10, 10, img_width, img_height);
}


// serialEvent runs everytime a serial message is sent
// I'm not going to comment this since we prefer to use Python and osc
public void serialEvent(Serial p) {
  
  inString = (myPort.readString());
  println(inString);  
  
  try {
    //Parse the data
    String[] dataStrings = split(inString, ',');
    
    // the pressure from mPa to Pa is coming in at a slower rate
    pressure = PApplet.parseFloat(dataStrings[1])/1000.0f;   
    
    // acceleration from mg to g
    accData.get(0).setCurVal(PApplet.parseFloat(dataStrings[2])/1000.0f);      
    accData.get(1).setCurVal(PApplet.parseFloat(dataStrings[3])/1000.0f);
    accData.get(2).setCurVal(PApplet.parseFloat(dataStrings[4])/1000.0f);
    
    // magnetometer data in \u00b5T
    magData.get(0).setCurVal(PApplet.parseFloat(dataStrings[5])/16.0f);      
    magData.get(1).setCurVal(PApplet.parseFloat(dataStrings[6])/16.0f);
    magData.get(2).setCurVal(PApplet.parseFloat(dataStrings[7])/16.0f);
    
    // gyroscope data in degrees per second
    gyroData.get(0).setCurVal(PApplet.parseFloat(dataStrings[8])/16.0f);      
    gyroData.get(1).setCurVal(PApplet.parseFloat(dataStrings[9])/16.0f);
    gyroData.get(2).setCurVal(PApplet.parseFloat(dataStrings[10])/16.0f);
       
    // Euler angles in degrees    
    x_angle = PApplet.parseFloat(dataStrings[13])/16.0f;
    y_angle = PApplet.parseFloat(dataStrings[12])/16.0f;
    z_angle = PApplet.parseFloat(dataStrings[11])/16.0f;
    heading = PApplet.parseFloat(dataStrings[11])/16.0f;
    
    // the orientation quaternion
    quat_w = PApplet.parseFloat(dataStrings[14])/16384.0f;
    quat_x = PApplet.parseFloat(dataStrings[15])/16384.0f;
    quat_y = PApplet.parseFloat(dataStrings[16])/16384.0f;
    quat_z = PApplet.parseFloat(dataStrings[17])/16384.0f;
    float norm = PApplet.sqrt(quat_x * quat_x + quat_y * quat_y + quat_z
                * quat_z +quat_w * quat_w);
    quat_w = quat_w/norm;
    quat_x = quat_x/norm;
    quat_y = quat_y/norm;
    quat_z = quat_z/norm;  
    println(norm);
        
    // linear acceleration in mg    
    lin_acc_x = PApplet.parseFloat(dataStrings[18]);
    lin_acc_y = PApplet.parseFloat(dataStrings[19]);
    lin_acc_z = PApplet.parseFloat(dataStrings[20]);
    
    // gravitation vector from mg to g
    grav_x = PApplet.parseFloat(dataStrings[21])/1000.0f;
    grav_y = PApplet.parseFloat(dataStrings[22])/1000.0f; 
    grav_z = PApplet.parseFloat(dataStrings[23])/1000.0f;
    
    // the calibration status
    calib_status = "Mag: " + dataStrings[24] + " - Acc: " + dataStrings[25] + " - Gyro: " + dataStrings[26] + " - System: " + dataStrings[27];
                
  } catch (Exception e) {
      println("Error while reading serial data.");
  }
}


// oscEvent runs everytime a message is sent from Python over the osc
public void oscEvent(OscMessage theOscMessage) {
  // osc message received
  println("### received an osc message with addrpattern "+theOscMessage.addrPattern()+" and typetag "+theOscMessage.typetag());
  // if the message address indicates the message has sensordata
  if (theOscMessage.addrPattern().equals("/sensordata")){
    //theOscMessage.print();}
    try{
      // This sections reads all of the sensor data from the osc message and stores it
      // The osc data is sent as an ArrayList, so the get function gets each data point.
      // Here is a map of the osc message data structure in index:measurement pairs
      /*
      1:pressure
      2,3,4:acceleration x,y,z
      5,6,7:magnetometer x,y,z
      8,9,10:gyro/angular velocity x,y,z
      11,12,13:heading, roll, pitch
      14,15,16,17:quaternion x,y,z,w
      18,19,20:linear acceleration x,y,z
      21,22,23:gravity x,y,z
      24,25,26,27:sensor calibration status
      */
      
      // the pressure from mPa to Pa is coming in at a slower rate
      pressure = theOscMessage.get(1).floatValue();
      
      // acceleration from mg to g
      accData.get(0).setCurVal(theOscMessage.get(2).floatValue()/1000.0f);      
      accData.get(1).setCurVal(theOscMessage.get(3).floatValue()/1000.0f);
      accData.get(2).setCurVal(theOscMessage.get(4).floatValue()/1000.0f);
      
      // magnetometer data in \u00b5T
      magData.get(0).setCurVal(theOscMessage.get(5).floatValue());      
      magData.get(1).setCurVal(theOscMessage.get(6).floatValue());
      magData.get(2).setCurVal(theOscMessage.get(7).floatValue());
      
      // gyroscope data in degrees per second
      gyroData.get(0).setCurVal(theOscMessage.get(8).floatValue());      
      gyroData.get(1).setCurVal(theOscMessage.get(9).floatValue());
      gyroData.get(2).setCurVal(theOscMessage.get(10).floatValue());
      
      // Euler angles in degrees    
      x_angle = theOscMessage.get(13).floatValue();
      y_angle = theOscMessage.get(12).floatValue();
      z_angle = theOscMessage.get(11).floatValue();
      heading = theOscMessage.get(11).floatValue();
      
      // the orientation quaternion
      quat_w = theOscMessage.get(14).floatValue();
      quat_x = theOscMessage.get(15).floatValue();
      quat_y = theOscMessage.get(16).floatValue();
      quat_z = theOscMessage.get(17).floatValue();
      // the magnitude of the quaternion 4D vector?
      float norm = PApplet.sqrt(quat_x * quat_x + quat_y * quat_y + quat_z
                  * quat_z +quat_w * quat_w);     
      quat_w = quat_w/norm;
      quat_x = quat_x/norm;
      quat_y = quat_y/norm;
      quat_z = quat_z/norm;  
      println(norm);
      
      // linear acceleration in mg    
      lin_acc_x = theOscMessage.get(18).floatValue();
      lin_acc_y = theOscMessage.get(19).floatValue();
      lin_acc_z = theOscMessage.get(20).floatValue();
      
      // gravitation vector from mg to g
      grav_x = theOscMessage.get(21).floatValue();
      grav_y = theOscMessage.get(22).floatValue(); 
      grav_z = theOscMessage.get(23).floatValue();
      
      // the calibration status
      calib_status = "Mag: " + str(theOscMessage.get(24).intValue()) + " - Acc: " + str(theOscMessage.get(25).intValue()) 
            + " - Gyro: " + str(theOscMessage.get(26).intValue()) + " - System: " + str(theOscMessage.get(27).intValue());
    }catch(Exception e){
      println("Error while receiving OSC sensor data");
    }
  }
}


// used to draw the green box for orientation representation
public void draw_rect(int r, int g, int b) {
  scale(100);
  // marks beginning of the box shape
  // passes in QUADS to indicate the drawing of quadrilaterals
  beginShape(QUADS);
  
  // set color to whatever was passed in, green above
  fill(r, g, b);
  // Here, the function defines all of the vertices of he rectangular prism.
  // You may think it would only have 8 vertices, but by specifying only 6 
  // Processing might draw the faces incorrectly, e.g. diagonally through the
  // box. Instead, we define 4 vertices at a time to each make a face. 6 of 
  // those 4-vertex chunk makes 6 faces for the rectangular prism
  vertex(-1,  1.5f,  0.25f);
  vertex( 1,  1.5f,  0.25f);
  vertex( 1, -1.5f,  0.25f);
  vertex(-1, -1.5f,  0.25f);

  vertex( 1,  1.5f,  0.25f);
  vertex( 1,  1.5f, -0.25f);
  vertex( 1, -1.5f, -0.25f);
  vertex( 1, -1.5f,  0.25f);

  vertex( 1,  1.5f, -0.25f);
  vertex(-1,  1.5f, -0.25f);
  vertex(-1, -1.5f, -0.25f);
  vertex( 1, -1.5f, -0.25f);

  vertex(-1,  1.5f, -0.25f);
  vertex(-1,  1.5f,  0.25f);
  vertex(-1, -1.5f,  0.25f);
  vertex(-1, -1.5f, -0.25f);

  vertex(-1,  1.5f, -0.25f);
  vertex( 1,  1.5f, -0.25f);
  vertex( 1,  1.5f,  0.25f);
  vertex(-1,  1.5f,  0.25f);

  vertex(-1, -1.5f, -0.25f);
  vertex( 1, -1.5f, -0.25f);
  vertex( 1, -1.5f,  0.25f);
  vertex(-1, -1.5f,  0.25f);

  endShape();
  
}


// These two functions, quat_rotate and quaternion_rotate are weird quaternion
// functions involved with using quaternion measurements to generate rotation.
// Don't worry about how they work, just know that they use the quaternion
// measurements collected by the Pozyx to make radian rotations that Processing
// can understand and use to rotate the green box as a Pozyx rotates.
public void quat_rotate(float w, float x, float y, float z) {
   float _x, _y, _z;
   //if (q1.w > 1) q1.normalise(); // if w>1 acos and sqrt will produce errors, this cant happen if quaternion is normalised
   double angle = 2 * Math.acos(w);
   float s = (float)Math.sqrt(1-w*w); // assuming quaternion normalised then w is less than 1, so term always positive.
   if (s < 0.001f) { // test to avoid divide by zero, s is always positive due to sqrt
     // if s close to zero then direction of axis not important
     _x = x; // if it is important that axis is normalised then replace with x=1; y=z=0;
     _y = y;
     _z = z;
   } else {
     _x = x / s; // normalise axis
     _y = y / s;
     _z = z / s;
   }
   rotate((float)angle, _x, _y, _z);     
}

public final PVector quaternion_rotate(float w, float x, float y, float z, PVector v) { 
      
      float q00 = 2.0f * x * x;
      float q11 = 2.0f * y * y;
      float q22 = 2.0f * z * z;

      float q01 = 2.0f * x * y;
      float q02 = 2.0f * x * z;
      float q03 = 2.0f * x * w;

      float q12 = 2.0f * y * z;
      float q13 = 2.0f * y * w;

      float q23 = 2.0f * z * w;

      return new PVector((1.0f - q11 - q22) * v.x + (q01 - q23) * v.y
                      + (q02 + q13) * v.z, (q01 + q23) * v.x + (1.0f - q22 - q00) * v.y
                      + (q12 - q03) * v.z, (q02 - q13) * v.x + (q12 + q03) * v.y
                      + (1.0f - q11 - q00) * v.z);
      
}
  public void settings() {  size(1100,800, P3D); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "pozyx_orientation3D_PSU" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
