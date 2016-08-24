package com.topd;

public class Fibonacci {
  static {
    System.loadLibrary("JniDll");
  }

  public int cal1(int num) {
    if (num <= 0) {
      return 0;
    } else if (num == 1) {
      return 1;
    }
    return this.cal1(num - 1) + this.cal1(num - 2);
  }

  public int cal2(int num) {
    if (num <= 0) {
      return 0;
    } else if (num == 1) {
      return 1;
    }

    int n0 = 0;
    int n1 = 1;
    int r = 0;
    int i = 2;
    while (i <= num) {
      r = n0 + n1;
      n0 = n1;
      n1 = r;
      i++;
    }
    return n1;
  }

  public native int cal3(int num);

  public static void main(String[] argv) {
    Fibonacci fib = new Fibonacci();
    System.out.println(fib.cal1(30));
    System.out.println(fib.cal2(30));
    System.out.println(fib.cal3(30));
  }

}
