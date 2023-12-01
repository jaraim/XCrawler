import numpy as np
class Stock:
     def __init__(self,nums):
        self.Time = nums[0]# 10点之前打到预测ma5直接买，下午就缓缓
        # 当前价格
        self.CurrentValue = nums[1]
        # 60日内的收盘价格列表
        self.CloseValues = nums[2]
        # 60日内的开盘价格列表
        self.OpenValues = nums[3]
        self.MaxValues = nums[4]
        self.MinValues = nums[5]
        # 60内，30日，20日，10日，5日均线价格
        self.MA5s = nums[6]
        self.MA10s = nums[7]
        self.MA20s = nums[8]
        self.MA30s = nums[9]
        self.MA60s = nums[10]
        
        # 换手率
        self.turnoverRates = nums[11]
        
        # 止盈卖出系数
        self.TakeProfit = 1.1
        # 止损卖出系数
        self.StopLoss = 0.97
        
        self.Calculate5_predict(self,s=1.099)
     
     # 计算移动平均函数
     def moving_average(data, window):
         weights = np.repeat(1.0, window) / window
         ma = np.convolve(data, weights, 'valid')
         return ma  

     def CalculateAverage(self,num):
         nums = self.CloseValues
         return self.moving_average(self.CloseValues,num)

     # 上一个交易日是否是跌势
     def IsFallYesterday(self):
         value = self.CloseValues[1]
         open = self.OpenValues[1]
         return value <open
     
     # 当前交易日是否是跌势
     def IsFallToday(self):
         value = self.CloseValues[0]
         open = self.OpenValues[0]
         return value <open

     # 预测明天5日线价格,可能是阶段低点
     def Calculate5_predict(self,s=1.099):
         self.predictValue = (self.CloseValues[0]*s+self.CloseValues[0]+self.CloseValues[1]+self.CloseValues[2]+self.CloseValues[3])/5
         return self.predictValue
     # =========== 短线逻辑
     # 龙头低吸算法1（预测5日线买入算法）
     def CheckBuyByPredict(self):
          return self.CurrentValue < self.predictValue

     # 龙头低吸算法2（5日线-10日线检测买入算法）          
     def CheckBuy(self):
         currentValue = self.CurrentValue
         # 只有连续5板以上
         # 只有在昨天下跌的情况下
         if self.IsFallYesterday():         
           MA5 = self.MA5s[0]
           MA10 = self.MA10s[0]
           if currentValue > MA5:
              return False
            # 触摸5日线 
           elif currentValue == MA5:
               return True
            # 击穿5日线，就以10日线为准
           elif currentValue < MA5 :
                # 在5-10日线之间，没有支撑位，破位！
                if currentValue > MA10:
                   return False
                # 触摸到10日线，找到10日线
                elif currentValue == MA10 :
                    return True
                # 10日线以下，放弃
                else:
                    return False
                
     # 卖出逻辑           
     def CheckSell(self,value):
         # value 传入当前成本价
         return self.CurrentValue >= value * self.TakeProfit or self.CurrentValue <= value * self.StopLoss
     
     # 长线逻辑(趋势逻辑)
     # 判断趋势的逻辑
     def detect_trend(ma5s, ma10s, ma20s):
         trend = []
         for i in range(len(ma5s)):
            if ma5s[i] > ma10s[i] and ma5s[i] > ma20s[i]:
               trend.append("上涨")
            elif ma5s[i] < ma10s[i] and ma5s[i] < ma20s[i]:
               trend.append("下跌")
            else:
               trend.append("震荡")
         return trend
     
     # 箱体逻辑 
     def checkBox(self,max,min):
         if self.CurrentValue >= max:
             return True
         elif self.CurrentValue <= min:
             return False
         else:
             return False
         
     # 破位逻辑
     def checkBroken(self,ma5,ma10,ma20,ma30,ma60):
         closeValue = self.CloseValues[0]
         if(closeValue<ma5):
             print("破5日线")
         elif(closeValue<ma10):
             print("破10日线")
         elif(closeValue<ma20):
             print("破20日线")
         elif(closeValue<ma30):
             print("破30日线")
         elif(closeValue<ma60):
             print("破60日线")
         
         
     # boll逻辑 todo
         

# # 计算MA5、MA10和MA20
# ma5 = moving_average(prices, 5)
# ma10 = moving_average(prices, 10)
# ma20 = moving_average(prices, 20)
# 执行趋势判断
# trend = detect_trend(ma5, ma10, ma20)   
    
     def Update(self,value):
         self.CurrentValue = value
         return self.CheckBuyByPredict()
        #  return self.CheckBuyValue(self)
     