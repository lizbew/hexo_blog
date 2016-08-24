#include <jni.h>
#include "com_topd_Fibonacci.h"

JNIEXPORT jint JNICALL Java_com_topd_Fibonacci_cal3
  (JNIEnv *env, jobject obj, jint num)
{
	long n0 = 0, n1 = 1, r, i;
	if (num <= 0)
	{
		return 0;
	} else if (num == 1)
	{
		return 1;
	}
	for (i = 2; i <= num; i++)
	{
		r = n0 + n1;
		n0 = n1;
		n1 = r;
	}
	return r;
}

