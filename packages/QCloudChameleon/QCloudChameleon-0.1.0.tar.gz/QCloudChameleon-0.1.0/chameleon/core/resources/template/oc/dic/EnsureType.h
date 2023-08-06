# coding: UTF-8
//
//  BWEnsureType.h
//  BWEnsureType
//
//  Created by tencent
//  Copyright (c) 2015年 tencent. All rights reserved.
//

#ifndef chameleonDemo_EnsureType_h
#define chameleonDemo_EnsureType_h
FOUNDATION_EXTERN char ensureCharType(id value);
FOUNDATION_EXTERN unsigned char ensureUnsignedCharType(id value);
FOUNDATION_EXTERN int ensureIntType(id value);
FOUNDATION_EXTERN unsigned int ensureUnsignedIntType(id value);
FOUNDATION_EXTERN short ensureShortType(id value);
FOUNDATION_EXTERN unsigned short ensureUnsignedShortType(id value);
FOUNDATION_EXTERN long ensureLongType(id value);
FOUNDATION_EXTERN unsigned long ensureUnsignedLongType(id value);
FOUNDATION_EXTERN long long ensureLongLongType(id value);
FOUNDATION_EXTERN unsigned long long ensureUnsignedLongLongType(id value);
FOUNDATION_EXTERN NSInteger ensureIntegerType(id value);
FOUNDATION_EXTERN NSUInteger ensureUIntegerType(id value);
FOUNDATION_EXTERN float ensureFloatType(id value);
FOUNDATION_EXTERN double ensureDoubleType(id value);
FOUNDATION_EXTERN BOOL ensureBoolType(id value);
FOUNDATION_EXTERN NSString * ensureStringType(id value);
FOUNDATION_EXTERN NSNumber * ensureNumberType(id value);
FOUNDATION_EXTERN NSURL * ensureURLType(id value);
FOUNDATION_EXTERN NSData * ensureDataType(id value);
FOUNDATION_EXTERN NSDictionary * ensureDictionaryType(id value);
FOUNDATION_EXTERN NSArray *ensureArrayType(id value);
#endif
