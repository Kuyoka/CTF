#include <stdio.h>
#include <windows.h>
#include <stdlib.h>
#include <string.h>
 
unsigned char esiData[17] = {0};
#define __ROL2__(x, n)  (((x) << (n)) | ((x) >> (16-(n))))
int check(unsigned char* esiData,WORD *calc_r)
{
    WORD k_E_D; // ST5C_2
    WORD k_A_9; // ST58_2
    WORD k_C_B; // di
    WORD k_0_F; // ST54_2
    WORD k_6_5; // ST60_2
    WORD k_2_1; // edx
    WORD k_8_7; // ebx
    WORD k_4_3; // ST48_4
    WORD v14; // eax
    WORD v17; // edx
    WORD v18; // eax
    WORD v19; // eax
    WORD v20; // ST00_2
    WORD v22; // ecx
    WORD result; // eax
 
    k_2_1 = esiData[0x1] + (esiData[0x2] << 8);
    k_4_3 = esiData[0x3] + (esiData[0x4] << 8);
    k_6_5 = esiData[0x5] + (esiData[0x6] << 8);
    k_8_7 = esiData[0x7] + (esiData[0x8] << 8);
    k_A_9 = esiData[0x9] + (esiData[0xA] << 8);
    k_C_B = esiData[0xB] + (esiData[0xC] << 8);
    k_E_D = esiData[0xD] + (esiData[0xE] << 8);
    k_0_F = esiData[0xF] + (esiData[0x0] << 8);
 
    WORD t0 = k_2_1 ^ k_4_3;
    WORD t1 = k_6_5 ^ k_8_7;
    WORD t2 = k_C_B - k_A_9;
    WORD t3 = k_0_F + k_E_D;
 
    WORD x1 = ((((t1 & 0x5555) + ((t1 >> 1) & 0x5555)) & 0x3333)     + ((((t1 & 0x5555) + ((t1 >> 1) & 0x5555)) >> 2) & 0x3333));
    x1 = ((((x1 & 0xF0F) + ((x1 >> 4) & 0xF0F)) >> 8) + ((x1 & 0xF) + ((x1 >> 4) & 0xF)));
 
    v14 = (t2 & ~t0 | t3 & t0);
 
    v17 = (t0 * v14 >> x1) + 24;
    v19 = t2 ^ v17;
    v20 = v14 | v17;
    v22 = v14 & v17 | (v19 & v20);
 
    calc_r[0] = k_4_3 ^ v22;                       // 0 4B 43    434B
    calc_r[1] = k_2_1 ^ v22;                       // 2 54 64    6454
    calc_r[2] = k_0_F + v19;                       // 4 1A 00    001A
    calc_r[3] = k_E_D - v19;                       // 6 19 18    1819
    calc_r[4] = k_C_B + v17;                       // 8 17 16    1617
    calc_r[5] = k_A_9 + v17;                       // A 15 14    1415
    calc_r[6] = __ROL2__(v14 ^ k_8_7, x1 & 0xFF);  // C 13 12    1213 
    calc_r[7] = __ROL2__(v14 ^ k_6_5, x1 & 0xFF);  // E 11 10    1011 
 
    return 1;                                      
    //  K  C  T  F 
    // 4B 43 54 46 00 1A 19 18 17 16 15 14 13 12 11 10
 
}
 
//十六进制字符串转换为字节流 
void HexStrToByte(const char* source, unsigned char* dest, int sourceLen)
{
    short i;
    unsigned char highByte, lowByte;
 
    for (i = 0; i < sourceLen; i += 2)
    {
        highByte = toupper(source[i]);
        lowByte = toupper(source[i + 1]);
 
        if (highByte > 0x39)
            highByte -= 0x37;
        else
            highByte -= 0x30;
 
        if (lowByte > 0x39)
            lowByte -= 0x37;
        else
            lowByte -= 0x30;
 
        dest[i / 2] = (highByte << 4) | lowByte;
    }
    return;
}
 
// This is an example of an exported function.
int main(void)
{
    /*
    UserName: BE1C6CB1F1616083
    Key: 5E2BA658A0E9C5F1B52C4C3C4C5C161C
    */
    char KCTF[32] = { 0x4B, 0x43, 0x54, 0x46, 0x00, 0x1A, 0x19, 0x18, 0x17, 0x16, 0x15, 0x14, 0x13, 0x12, 0x11, 0x10 };
    char username[32] = { 0x1F, 0x1E, 0x1D, 0x1C, 0x1B, 0x1A, 0x19, 0x18, 0x17, 0x16, 0x15, 0x14, 0x13, 0x12, 0x11, 0x10 };
    printf("Input user name: ");
    scanf("%s", username);
    char passwd[64] = { 0 };
    WORD calc_result[9] = { 0 };
    printf("Input password: ");
    scanf("%s", passwd);
    //memcpy(username,"BE1C6CB1F1616083",16);
    //memcpy(passwd, "5E2BA658A0E9C5F1B52C4C3C4C5C161C", 32);
    //memcpy(username, KCTF,16);
    //memcpy(passwd, "6CCDE9D2EC1D469DC67C647E66B4C565", 32);
    int len = strlen(passwd);
    HexStrToByte(passwd, esiData , len);
 
    int result1 = check(esiData, calc_result);
 
    int result = memcmp(username, (char*)calc_result, 0x10);
    if (!result)
        printf("Success!\r\n");
    else
        printf("Error!\r\n");
 
    system("pause");
    return 0;
}