---
title: Create Walle with arduino
date: 2019-02-23 00:41:24
tags: [arduino,  Protothreads]
---

很早之前想给LH做个电子小玩意， 于是买了几个Arduino Nano的小板子开始玩了。 想象中的外形是瓦力Walle的小车， 有前进的车轮、有挥动的手臂，但多个舵机实现难度太大，且手臂、车轮的零配件不好找， 最终削减到只用基础元件来做个能摇头的小呆呆。

涉及到多个器件同时控制，开始引入了Arduino-FreeRTOS (https://github.com/feilipu/Arduino_FreeRTOS_Library), 使用三个任务运行时出了问题不知道啥原因，也不好定位，于是不得不放弃了。 于是改用 Protothreads (http://dunkels.com/adam/pt/api.html), 现在用起来很顺利。

现在这个只能连接USB充电线才能运行， 考虑使用18860 3.7v锂电池，再加一个升压模块到5v。 计划总没有变化快， 小呆呆估计是送不出去了， 只能留着自己玩，电源的事先不想折腾了， 等下次再想买器件时再从某宝入手。

## 集成的组件列表

* Arduino Nano
* ssd1306 - 128*64 OLED显示屏, I2C接口
* DS18B20 -  温度传感器
* DS1302 - 实时时钟， 使用带钮扣电池的
* SG90 - 9g 舵机
* HC-SR40 - 距离传感器
* 红色LED， 按钮
 

## 一些参考网页
* 舵机 https://www.arduino.cn/thread-1038-1-1.html,  https://www.arduino.cc/en/Reference/Servo
* 电源 http://arduino.nxez.com/2019/01/03/scrolling-text-display-with-arduino-a-to-z-guide.html
* LED  https://jingyan.baidu.com/article/a65957f4e358d924e67f9bad.html， https://zhuanlan.zhihu.com/p/37637038
  

## 接口端口


<table>
<tr><th style="width:200px">Arduino Nano端口</th><th>器件接口</th><th>说明</th></tr>
<tr><td>-<br>-<br>D2</td> <td>GND（黑）<br>VCC（红）- 5v<br>Signal（黄）<br></td> <td>g9 舵机</td></tr>
<tr><td>-<br>D3<br>D4<br>-</td> <td>VCC - 3.3v/5v<br>TRIG<br>ECHO<br>GND</td>   <td>HC-SR04 距离传感器</td></tr>
<tr><td>-<br>D5<br>-</td> <td>VCC - 5v<br>dat<br>-</td>   <td>DS18B20 温度传感器</td></tr>
<tr><td>-<br>-<br>D6<br>D7<br>D8<br></td> <td>VCC - 3.3v/5v<br>GND<br>CLK<br>DAT<br>RST</td>   <td>DS1302 时钟模块 </td></tr>
<tr><td>D9</td> <td>LED</td>   <td>接1K 电阻， 高电平触发</td></tr>
<tr><td>D10</td> <td>按键</td>   <td>接10K电阻， 读高电平</td></tr>
<tr><td>-<br>-<br>A5<br>A4</td> <td>Vcc<br>GND<br>SCL<br>SDA</td>   <td>ssd1306, 0.96寸 OLED, I2C接口</td></tr>
</table>


## 使用的组件库

* Protothreads - http://dunkels.com/adam/pt/api.html
* Servo - https://www.arduino.cc/en/Reference/Servo
* DS18B20
  * OneWire Library - https://www.pjrc.com/teensy/td_libs_OneWire.html
  * Arduino-Temperature-Control-Library - https://github.com/milesburton/Arduino-Temperature-Control-Library
* DS1302 - https://github.com/msparks/arduino-ds1302
* u8g2 - https://github.com/olikraus/u8g2/wiki

