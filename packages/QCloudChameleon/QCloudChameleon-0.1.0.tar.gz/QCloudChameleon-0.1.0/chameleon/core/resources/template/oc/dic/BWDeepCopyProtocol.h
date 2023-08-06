# coding: UTF-8
//
//  BWDeepCopyProtocol.h
//  chameleonDemo
//
//  Created by liujin on 15/8/28.
//  Copyright © 2015年 LiuJin. All rights reserved.
//

#import <Foundation/Foundation.h>

@protocol BWDeepCopyProtocol <NSObject>
@property (nonatomic, strong, readonly) id deepCopy;
@end
