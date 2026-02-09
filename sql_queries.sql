- Blueprint Technologies Revenue Operations SQL Queries

-- 1. Revenue Performance by Region and Quarter
SELECT 
    Region,
    Quarter,
    SUM(Actual_Revenue) as Total_Revenue,
    COUNT(Opportunity_ID) as Deal_Count,
    AVG(Deal_Size) as Avg_Deal_Size,
    SUM(CASE WHEN Sales_Stage = 'Closed Won' THEN Actual_Revenue ELSE 0 END) as Won_Revenue
FROM revenue_opportunities
GROUP BY Region, Quarter
ORDER BY Region, Quarter;

-- 2. Pipeline Health Analysis
SELECT 
    Sales_Stage,
    COUNT(Opportunity_ID) as Opportunity_Count,
    SUM(Deal_Size) as Pipeline_Value,
    AVG(Probability) as Avg_Probability,
    SUM(Expected_Revenue) as Weighted_Pipeline
FROM revenue_opportunities
WHERE Sales_Stage NOT IN ('Closed Won', 'Closed Lost')
GROUP BY Sales_Stage
ORDER BY AVG(Probability) DESC;

-- 3. Channel Performance and ROI
SELECT 
    Channel,
    SUM(Actual_Revenue) as Total_Revenue,
    COUNT(Opportunity_ID) as Total_Deals,
    SUM(Actual_Revenue)/COUNT(Opportunity_ID) as Revenue_Per_Deal,
    SUM(CASE WHEN Sales_Stage = 'Closed Won' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) as Win_Rate
FROM revenue_opportunities
GROUP BY Channel
ORDER BY Total_Revenue DESC;

-- 4. Marketing Program Attribution
SELECT 
    Marketing_Program,
    SUM(Actual_Revenue) as Attributed_Revenue,
    COUNT(DISTINCT Opportunity_ID) as Influenced_Deals,
    AVG(Deal_Size) as Avg_Influenced_Deal_Size
FROM revenue_opportunities
GROUP BY Marketing_Program
HAVING SUM(Actual_Revenue) > 100000
ORDER BY Attributed_Revenue DESC;

-- 5. Quarterly Business Review Summary
SELECT 
    Quarter,
    Region,
    Product,
    SUM(Actual_Revenue) as Revenue,
    SUM(Expected_Revenue) as Forecast,
    SUM(Actual_Revenue) - SUM(Expected_Revenue) as Variance,
    (SUM(Actual_Revenue) - SUM(Expected_Revenue)) / SUM(Expected_Revenue) * 100 as Variance_Pct
FROM revenue_opportunities
GROUP BY Quarter, Region, Product
ORDER BY Quarter, Region;
