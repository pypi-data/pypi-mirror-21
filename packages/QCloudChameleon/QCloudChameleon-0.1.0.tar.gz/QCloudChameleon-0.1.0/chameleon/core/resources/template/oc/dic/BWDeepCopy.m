# coding: UTF-8
//
//  BWDeepCopy.m
//  chameleonDemo
//
//  Created by tencent on 15/9/1.
//  Copyright © 2015年 tencent. All rights reserved.
//

#import "BWDeepCopy.h"

@implementation NSObject (DeepCopy)

- (instancetype)deepCopy
{
    return self;
}

@end

@implementation NSDictionary (DeepCopy)

- (instancetype)deepCopy
{
    NSMutableDictionary *dic = [NSMutableDictionary dictionary];
    NSArray *allKeys = self.allKeys;
    for (NSString *key in allKeys) {
        NSObject<NSCopying> *value = [self valueForKey:key];
        if (value) {
            if ([value isKindOfClass:[NSDictionary class]] || [value isKindOfClass:[NSArray class]]) {
                [dic setObject:value.deepCopy forKey:key];
            }
            else
            {
                [dic setObject:value.copy forKey:key];
            }
        }
    }
    return dic;
}

@end

@implementation NSArray (DeepCopy)

- (instancetype)deepCopy
{
    NSMutableArray *array = [NSMutableArray array];
    for (NSObject<NSCopying> *value in self) {
        if (value) {
            if ([value isKindOfClass:[NSDictionary class]] || [value isKindOfClass:[NSArray class]]) {
                [array addObject:value.deepCopy];
            }
            else
            {
                [array addObject:value.copy];
            }
        }
    }
    return array;
}

@end