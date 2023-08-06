# coding: UTF-8
//
//  BWTODictionary.m
//  chameleonDemo
//
//  Created by liujin on 15/9/1.
//  Copyright © 2015年 LiuJin. All rights reserved.
//

#import "BWTODictionary.h"

@implementation NSObject (TODictionary)
- (id)toDictionaryValue
{
    return self;
}
- (id)toServerDictionaryValue
{
    return self;
}
@end

@implementation NSDictionary (TODictionary)
- (id)toDictionaryValue
{
    NSMutableDictionary *dic = [NSMutableDictionary dictionary];
    NSArray *allKeys = self.allKeys;
    for (NSString *key in allKeys) {
        id value = [self valueForKey:key];
        if (value) {
            [dic setObject:[value toDictionaryValue] forKey:key];
        }
    }
    return dic;
}
- (id)toServerDictionaryValue
{
    NSMutableDictionary *dic = [NSMutableDictionary dictionary];
    NSArray *allKeys = self.allKeys;
    for (NSString *key in allKeys) {
        id value = [self valueForKey:key];
        if (value) {
            [dic setObject:[value toServerDictionaryValue] forKey:key];
        }
    }
    return dic;
}
@end

@implementation NSArray (TODictionary)
- (id)toDictionaryValue
{
    NSMutableArray *array = [NSMutableArray array];
    for (id value in self) {
        if (value) {
            [array addObject:[value toDictionaryValue]];
        }
    }
    return array;
}
- (id)toServerDictionaryValue
{
    NSMutableArray *array = [NSMutableArray array];
    for (id value in self) {
        if (value) {
            [array addObject:[value toServerDictionaryValue]];
        }
    }
    return array;
}
@end

@implementation NSURL (TODictionary)
- (id)toDictionaryValue
{
    return [self absoluteString];
}
- (id)toServerDictionaryValue
{
    return [self absoluteString];
}
@end

@implementation NSData (TODictionary)
- (id)toDictionaryValue
{
    return [[NSString alloc] initWithData:(NSData *)self encoding:NSUTF8StringEncoding];
}
- (id)toServerDictionaryValue
{
    return [[NSString alloc] initWithData:(NSData *)self encoding:NSUTF8StringEncoding];
}

@end

