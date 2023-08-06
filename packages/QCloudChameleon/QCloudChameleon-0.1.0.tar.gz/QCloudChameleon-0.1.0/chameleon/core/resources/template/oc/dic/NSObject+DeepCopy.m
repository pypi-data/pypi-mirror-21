# coding: UTF-8
//
//  NSObject+DeepCopy.m
//  chameleonDemo
//
//  Created by liujin on 15/8/28.
//  Copyright © 2015年 LiuJin. All rights reserved.
//

#import "NSObject+DeepCopy.h"

@implementation NSObject (DeepCopy) 
- (id)deepCopy
{
    if ([self isKindOfClass:[NSDictionary class]]) {
        // NSDictionary
        NSMutableDictionary *dic = [NSMutableDictionary dictionary];
        NSArray *allKeys = ((NSDictionary *)self).allKeys;
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
    if ([self isKindOfClass:[NSArray class]]) {
        // NSArray
        NSMutableArray *array = [NSMutableArray array];
        for (NSObject<NSCopying> *value in (NSArray *)self) {
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
    return self;
}

@end
