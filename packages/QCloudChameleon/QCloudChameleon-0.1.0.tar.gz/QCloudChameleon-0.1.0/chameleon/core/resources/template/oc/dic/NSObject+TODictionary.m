# coding: UTF-8
//
//  NSObject+TODictionary.m
//  chameleonDemo
//
//  Created by tencent
//  Copyright (c) 2015年 tencent. All rights reserved.
//

#import "NSObject+TODictionary.h"

@implementation NSObject (TODictionary)
- (id)toDictionaryValue
{
    if ([self isKindOfClass:[NSDictionary class]]) {
        NSMutableDictionary *dic = [NSMutableDictionary dictionary];
        NSArray *allKeys = ((NSDictionary *)self).allKeys;
        for (NSString *key in allKeys) {
            id value = [self valueForKey:key];
            if (value) {
                [dic setObject:[value toDictionaryValue] forKey:key];
            }
        }
        return dic;
    }
    if ([self isKindOfClass:[NSArray class]]) {
        NSMutableArray *array = [NSMutableArray array];
        for (id value in (NSArray *)self) {
            if (value) {
                [array addObject:[value toDictionaryValue]];
            }
        }
        return array;
    }
    if ([self isKindOfClass:[NSURL class]]) {
        return [(NSURL *)self absoluteString];
    }
    if ([self isKindOfClass:[NSData class]]) {
        return  [[NSString alloc] initWithData:(NSData *)self encoding:NSUTF8StringEncoding];
    }
    return self;
}

- (id)toServerDictionaryValue
{
    if ([self isKindOfClass:[NSDictionary class]]) {
        NSMutableDictionary *dic = [NSMutableDictionary dictionary];
        NSArray *allKeys = ((NSDictionary *)self).allKeys;
        for (NSString *key in allKeys) {
            id value = [self valueForKey:key];
            if (value) {
                [dic setObject:[value toDictionaryValue] forKey:key];
            }
        }
        return dic;
    }
    if ([self isKindOfClass:[NSArray class]]) {
        NSMutableArray *array = [NSMutableArray array];
        for (id value in (NSArray *)self) {
            if (value) {
                [array addObject:[value toDictionaryValue]];
            }
        }
        return array;
    }
    if ([self isKindOfClass:[NSURL class]]) {
        return [(NSURL *)self absoluteString];
    }
    if ([self isKindOfClass:[NSData class]]) {
        return  [[NSString alloc] initWithData:(NSData *)self encoding:NSUTF8StringEncoding];
    }
    return self;
}
@end
