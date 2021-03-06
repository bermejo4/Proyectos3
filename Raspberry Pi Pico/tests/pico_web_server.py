import utime
from machine import Pin, ADC, Signal
import uos
import rp2
from time import sleep
import time
from mpu6050 import MPU6050


def sendCMD_waitResp(cmd, uart=machine.UART(0, baudrate=115200), timeout=100):
    print("CMD: " + cmd)
    uart.write(cmd)
    resp=waitResp(uart, timeout)
    print()
    return resp
    
def waitResp(uart=machine.UART(0, baudrate=115200), timeout=100):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print("resp:")
    try:
        print(resp.decode())
    except UnicodeError:
        print(resp)
    return resp
        
# send CMD to uart,
# wait and show response without return
def sendCMD_waitAndShow(cmd, uart=machine.UART(0, baudrate=115200)):
    print("CMD: " + cmd)
    uart.write(cmd)
    while True:
        print(uart.readline())
        
def espSend(text="test", uart=machine.UART(0, baudrate=115200)):
    sendCMD_waitResp('AT+CIPSEND=' + str(len(text)) + '\r\n')
    sendCMD_waitResp(text)

def html_to_strigline_transformer(html):
    string_line=html.replace("\n","")
    return string_line
        
if __name__ == "__main__":    
    server_ip="192.168.20.10"
    server_port=9999
    
    print()
    print("Machine: \t" + uos.uname()[4])
    print("MicroPython: \t" + uos.uname()[3])

    #indicate program started visually
    led_onboard = machine.Pin(25, machine.Pin.OUT)
    led_onboard.value(0)     # onboard LED OFF/ON for 0.5/1.0 sec
    utime.sleep(0.5)
    led_onboard.value(1)
    utime.sleep(1.0)
    led_onboard.value(0)

    uart0 = machine.UART(0, baudrate=115200)
    print(uart0)
    
    sendCMD_waitResp('AT\r\n')          #Test AT startup
    sendCMD_waitResp('AT+CWMODE=3\r\n') #ESP-8266 WiFi module in Soft AP+ Station mode
    sendCMD_waitResp('AT+CWSAP="pos_softap","",11,0,3\r\n') #ssid, passwd, channel, encryp_mod, max_stations
    #encryp_mod: 0: OPEN//2: WPA_PSK//3: WPA2_PSK//4: WPA_WPA2_PSK
    sendCMD_waitResp('AT+CIPMUX=1\r\n') #enable multiple tcp connections //0:single connection
    sendCMD_waitResp('AT+CIPSERVER=1,80\r\n')
    
    sensor_temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    
    file = open("init_page.html", "r")
    html_code=str(file.read())
    print(html_code)
    file.close()
    
    while True:
        #temperature reading
        #reading_temp = sensor_temp.read_u16() * conversion_factor 
        #temperature = 27 - (reading_temp - 0.706)/0.001721
        #Place basic code for HTML page display
        #val='<head><title>Rasberry Pi Pico Server</title></head><body><p>Temperature is: '+str(int(temperature))+' deg'+'</p></body>'
        #val='<html> <head> <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> <link rel=\"stylesheet\" href=\"https://use.fontawesome.com/releases/v5.7.2/css/all.css\" integrity=\"sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr\" crossorigin=\"anonymous\"> <style> html { font-family: Arial; display: inline-block; margin: 0px auto; text-align: center; } .button { background-color: #ce1b0e; border: none; color: white; padding: 16px 40px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; } .button1 { background-color: #000000; } </style> </head> <body> <h2>Raspberry Pi Pico Web Server</h2> <p>LED state: <strong></strong></p> <p> <i class=\"fas fa-lightbulb fa-3x\" style=\"color:#c81919;\"></i> <a href=\\\"?led_on\\\"><button class=\"button\">LED ON</button></a> </p> <p> <i class=\"far fa-lightbulb fa-3x\" style=\"color:#000000;\"></i> <a href=\\\"?led_off\\\"><button class=\"button button1\">LED OFF</button></a> </p> </body> </html>'
        val=html_to_strigline_transformer(html_code)
        print(val)
        length=str(len(val))
        send='AT+CIPSEND=1,'+length+'\r\n'
        volcado1=sendCMD_waitResp(send)
        time.sleep(2)
        send=val+'\r\n'
        volcado2=sendCMD_waitResp(send)
        time.sleep(2)
        print()
        print('--------------------------------')
        print('volcado1:'+str(volcado1))
        print('--------------------------------')
        print()
        print('--------------------------------')
        print('volcado2:'+str(volcado2))
        print('--------------------------------')
        print()
        
 
    
    #sendCMD_waitResp('AT+CWLAP\r\n', timeout=5000) #List available APs
    #sendCMD_waitResp('AT+CWJAP="iot4",""\r\n', timeout=5000) #Connect to AP
    #sendCMD_waitResp('AT+CIFSR\r\n')    #Obtain the Local IP Address
    #sendCMD_waitResp('AT+CIPSTART="TCP","192.168.12.147",9999\r\n')
    #sendCMD_waitResp('AT+CIPSTART="TCP","' +
                 #server_ip +
                 #'",' +
                 #str(server_port) +
                 #'\r\n')
    #espSend()
    
#-----------------------------------------------------        
    #while True:
       # string_to_send=""
        #string_to_send=str(data_collector())
        #utime.sleep_ms(5)
        #utime.sleep_ms(int((1/FREQUENCY_SEND)*1000))
        #print('Enter something:')
        #msg = input()
        #sendCMD_waitResp('AT+CIPSTART="TCP","192.168.12.147",9999\r\n')
        #sendCMD_waitResp('AT+CIPSTART="TCP","' +
                     #server_ip +
                     #'",' +
                     #str(server_port) +
                     #'\r\n')
        #print("enviando:"+string_to_send)
        #espSend(string_to_send)