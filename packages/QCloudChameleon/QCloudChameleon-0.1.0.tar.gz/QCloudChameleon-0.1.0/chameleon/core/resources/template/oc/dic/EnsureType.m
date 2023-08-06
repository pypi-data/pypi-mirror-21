# coding: UTF-8
//
//  BWEnsureType.m
//  BWEnsureType
//
//  Created by tencent
//  Copyright (c) 2015年 tencent. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <Foundation/NSKeyedArchiver.h>

// 基本数据类型
// (char、unsigned char、int、unsigned int、short、unsigned short、long、unsigned long、longlong、unsigned long long、integer、uinteger、float、double、BOOL)

// char
char ensureCharType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return 0;
    }
    if ([value isKindOfClass:[NSNumber class]]) {
        return [value charValue];
    }
    // NSString ->char
    if ([value isKindOfClass:[NSString class]]) {
        NSScanner *scan = [NSScanner scannerWithString:value];
        int val;
        if ([scan scanInt:&val] && [scan isAtEnd]) {
            return (char)val;
        }
    }
    NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return 0;
}

// unsigned char
unsigned char ensureUnsignedCharType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return 0;
    }
    if ([value isKindOfClass:[NSNumber class]]) {
        return [value unsignedCharValue];
    }
    // NSString ->unsigned char
    if ([value isKindOfClass:[NSString class]]) {
         NSScanner *scan = [NSScanner scannerWithString:value];
        unsigned long long val;
        if ([scan scanUnsignedLongLong:&val] && [scan isAtEnd]) {
            return (unsigned char)val;
        }
    }
    NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return 0;
}

// int
int ensureIntType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return 0;
    }
    if ([value isKindOfClass:[NSNumber class]]) {
        return [value intValue];
    }
    // NSString ->int
    if ([value isKindOfClass:[NSString class]]) {
        NSScanner *scan = [NSScanner scannerWithString:value];
        int val;
        if ([scan scanInt:&val] && [scan isAtEnd]) {
            return val;
        }
    }
     NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return 0;
}

//unsigned int
unsigned int ensureUnsignedIntType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return 0;
    }
    if ([value isKindOfClass:[NSNumber class]]) {
        return [value unsignedIntValue];
    }
    // NSString ->unsigned int
    if ([value isKindOfClass:[NSString class]]) {
        NSScanner *scan = [NSScanner scannerWithString:value];
        unsigned long long val;
        if ([scan scanUnsignedLongLong:&val] && [scan isAtEnd]) {
            return (unsigned int)val;
        }
    }
    NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return 0;
}

// short
short ensureShortType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return 0;
    }
    if ([value isKindOfClass:[NSNumber class]]) {
        return [value shortValue];
    }
    // NSString ->short
    if ([value isKindOfClass:[NSString class]]) {
        NSScanner *scan = [NSScanner scannerWithString:value];
        int val;
        if ([scan scanInt:&val] && [scan isAtEnd]) {
            return (short)val;
        }
    }
    NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return 0;
}

// unsigned short
unsigned short ensureUnsignedShortType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return 0;
    }
    if ([value isKindOfClass:[NSNumber class]]) {
        return [value unsignedShortValue];
    }
    // NSString ->unsigned short
    if ([value isKindOfClass:[NSString class]]) {
        NSScanner *scan = [NSScanner scannerWithString:value];
        unsigned long long val;
        if ([scan scanUnsignedLongLong:&val] && [scan isAtEnd]) {
            return (unsigned short)val;
        }
    }
    NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return 0;
}

// long
long ensureLongType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return 0;
    }
    if ([value isKindOfClass:[NSNumber class]]) {
        return [value longValue];
    }
    // NSString ->long
    if ([value isKindOfClass:[NSString class]]) {
        NSScanner *scan = [NSScanner scannerWithString:value];
        long long val;
        if ([scan scanLongLong:&val] && [scan isAtEnd]) {
            return (long)val;
        }
    }
    NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return 0;
}

// unsigned long
unsigned long ensureUnsignedLongType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return 0;
    }
    if ([value isKindOfClass:[NSNumber class]]) {
        return [value unsignedLongValue];
    }
    // NSString ->unsigned long
    if ([value isKindOfClass:[NSString class]]) {
        NSScanner *scan = [NSScanner scannerWithString:value];
        unsigned long long val;
        if ([scan scanUnsignedLongLong:&val] && [scan isAtEnd]) {
            return (unsigned long)val;
        }
    }
    NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return 0;
}

// long long
long long ensureLongLongType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return 0;
    }
    if ([value isKindOfClass:[NSNumber class]]) {
        return [value longLongValue];
    }
    // NSString ->long long
    if ([value isKindOfClass:[NSString class]]) {
        NSScanner *scan = [NSScanner scannerWithString:value];
        long long val;
        if ([scan scanLongLong:&val] && [scan isAtEnd]) {
            return val;
        }
    }
    NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return 0;
}

// unsigned longlong
unsigned long long ensureUnsignedLongLongType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return 0;
    }
    if ([value isKindOfClass:[NSNumber class]]) {
        return [value unsignedLongLongValue];
    }
    // NSString ->unsigned longlong
    if ([value isKindOfClass:[NSString class]]) {
        NSScanner *scan = [NSScanner scannerWithString:value];
        unsigned long long val;
        if ([scan scanUnsignedLongLong:&val] && [scan isAtEnd]) {
            return val;
        }
    }
    NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return 0;
}

// NSInteger
NSInteger ensureIntegerType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return 0;
    }
    if ([value isKindOfClass:[NSNumber class]]) {
        return [value integerValue];
    }
    // NSString->NSInteger
    if ([value isKindOfClass:[NSString class]]) {
        NSScanner *scan = [NSScanner scannerWithString:value];
        NSInteger val;
        if ([scan scanInteger:&val] && [scan isAtEnd]) {
            return val;
        }
    }
    NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return 0;
}

// NSUInteger
NSUInteger ensureUIntegerType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return 0;
    }
    if ([value isKindOfClass:[NSNumber class]]) {
        return [value unsignedIntegerValue];
    }
    // NSString ->NSUinteger
    if ([value isKindOfClass:[NSString class]]) {
        NSScanner *scan = [NSScanner scannerWithString:value];
        unsigned long long val;
        if ([scan scanUnsignedLongLong:&val] && [scan isAtEnd]) {
            return (NSUInteger)val;
        }
    }
    NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return 0;
}

// float
float ensureFloatType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return 0;
    }
    if ([value isKindOfClass:[NSNumber class]]) {
        return [value floatValue];
    }
    // NSString ->float
    if ([value isKindOfClass:[NSString class]]) {
        NSScanner *scan = [NSScanner scannerWithString:value];
        float val;
        if ([scan scanFloat:&val] && [scan isAtEnd]) {
            return val;
        }
    }
    NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return 0;
}
// double
double ensureDoubleType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return 0;
    }
    if ([value isKindOfClass:[NSNumber class]]) {
        return [value doubleValue];
    }
    // NSString ->double
    if ([value isKindOfClass:[NSString class]]) {
        NSScanner *scan = [NSScanner scannerWithString:value];
        double val;
        if ([scan scanDouble:&val] && [scan isAtEnd]) {
            return val;
        }
    }
    NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return 0;
}

// BOOL
BOOL ensureBoolType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return NO;
    }
    // NSNumber->BOOL
    if ([value isKindOfClass:[NSNumber class]]) {
        return [value boolValue];
    }
    // NSString->BOOL
    if ([value isKindOfClass:[NSString class]]) {
        if ([value isEqualToString:@"true"]) {
            return YES;
        }
        return NO;
    }
    NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return NO;
}

// object
// NSString NSNumber NSURL NSData NSDictionary NSArray

// NSString
NSString * ensureStringType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return nil;
    }
    if ([value isKindOfClass:[NSString class]]) {
        return  value;
    }
    // NSNumber->NSString
    if ([value isKindOfClass:[NSNumber class]])
    {
        return [value stringValue];
    }
    NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return nil;
}

// NSNumber
NSNumber * ensureNumberType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return nil;
    }
    if ([value isKindOfClass:[NSNumber class]])
    {
        return value;
    }
    // NSString->NSNumber
    if ([value isKindOfClass:[NSString class]])
    {
        NSNumberFormatter *numberFormatter = [[NSNumberFormatter alloc] init];
        return [numberFormatter numberFromString:value];
    }
    NSCAssert(([value isKindOfClass:[NSNumber class]]) || ([value isKindOfClass:[NSString class]]), @"数据不是NSNumber或者NSString类型，无法向自定义类型转换");
    return nil;
}

// NSURL
NSURL * ensureURLType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return nil;
    }
    // NSString->NSURL
    if ([value isKindOfClass:[NSString class]]) {
        return [NSURL URLWithString:(NSString *)value];
    }
    NSCAssert([value isKindOfClass:[NSString class]], @"数据不是NSString类型，无法向自定义类型转换");
    return nil;
}

// NSData
NSData * ensureDataType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return nil;
    }
    // NSString->NSData
    if ([value isKindOfClass:[NSString class]]) {
        return [(NSString*)value dataUsingEncoding:NSUTF8StringEncoding];
    }
    NSCAssert([value isKindOfClass:[NSString class]], @"数据不是NSString类型，无法向自定义类型转换");
    return nil;
}

// NSDictionary
NSDictionary * ensureDictionaryType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return nil;
    }
    if ([value isKindOfClass:[NSDictionary class]]) {
        return value;
    }
    NSCAssert([value isKindOfClass:[NSDictionary class]], @"数据不是NSDictionary类型，无法向自定义类型转换");
    return nil;
}

// NSArray
NSArray *ensureArrayType(id value)
{
    if ((!value) || ([value isKindOfClass:[NSNull class]])) {
        return nil;
    }
    if ([value isKindOfClass:[NSArray class]]) {
        return value;
    }
    NSCAssert([value isKindOfClass:[NSArray class]], @"数据不是NSArray类型，无法向自定义类型转换");
    return nil;
}

