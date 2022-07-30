#include <Servo.h>
  // Declaración de varibles para servos
Servo s_1;
Servo s_2;
Servo s_3;
Servo s_4;
  // Vector donde se guardarán los datos transformados 
int data[4];
  // Varible que guardará los datos recibidos
String serialData;
void setup() {
  // Declaración de baudios en comunicación serial
  Serial.begin(9600);
    // Declaración de pines para cada servo
  s_1.attach(8);
  s_2.attach(9);
  s_3.attach(10);
  s_4.attach(11);

}

void loop() {
  // Condicional para realizar acciones si recibe datos del puerto
  if (Serial.available()>0){
      // Guardamos datos enviados hasta el salto de línea
    serialData = Serial.readStringUntil('\n');
      // Ciclo para guardar los datos en el vector
    for (int i = 0; i<4; i++ ){
        // Solo leerá los datos hasta que encuentre una coma
      int ending = serialData.indexOf(",");
        // Al encotrarla extraerá el número
      data[i]=atol(serialData.substring(0,ending).c_str());
      serialData = serialData.substring(ending + 1);
      }
      //Los datos guardados se escribiran en cada servomotor
    s_1.write(data[0]);
    delay(1);
    s_2.write(data[1]);
    delay(1);
    s_3.write(data[2]);
    delay(1);
    s_4.write(data[3]);
    delay(1);
    
  }

}
