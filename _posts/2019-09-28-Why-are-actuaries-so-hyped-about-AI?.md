---
title: "Is this just all hype?"
layout: post
excerpt: ""
categories:
  - AI
  - Actuarial Science
tags:

last_modified_at: 2019-09-28T12:43:31-05:00
---

There is a lot of hype today around AI in the actuarial industry.  Here are the latest developments.

## AI is not just a recent trend

AI and Machine Learning are now buzzwords in the actuarial industry, but these methods have been on the radar for years.  For those of us who have entered the industry in the last few years, such as myself, it only feels as though this is a recent topic. 

Below is a summary of the actuarial literature from the SOA's [Predictive Analytics Section](https://www.soa.org/sections/pred-analytics-futurism/pred-analytics-futurism-landing/).  This is a research newsletter written by actuaries.  Deep Learning first appeared in 2014.  Machine Learning, which has gone by different names such as “forecasting” and “predictive modeling” has been around since 2012.

The term "predictive analytics" refers to how machine learning is applied to a business context.  I don't put this in the same context as AI because this generally refers to simpler problems, such as supervised machine learning models (GBMs, GLMs, RFs) which use tabular data in order to predict a known outcome.

![useful image]({{ site.url }}/assets/css/AI_in_industry_timeline.PNG)

## AI is going to change insurance like no other technology has

Deep learning has the ability to use data that no other algorithm can.  Video, audio, text, real-time sensor data such as electronic health records, and other non-traditional data sources can now be used in models.  

A few applications are:

**Video**
- Using vehicle video and sensor data to assess the damage in auto insurance.  Drivers that exhibit riskier behavior can be identified *before* they get into accidents, and safe drivers can be rewarded.  By 2030-2035, when self-driving cars are commonplace, there will be even more data available and traditional auto insurance will be obsolete.
- Cameras in front of retail stores that can record customer traffic patterns to be used for predicting general liability claims.  For example, if there are more people walking in and out of the store, it is more likely that a person will fall, injure themselves, and sue the retailer.
- Facial recognition cameras that record time and location of individuals.  There are many potential use cases for this.  [China](https://time.com/collection/davos-2019/5502592/china-social-credit-score/) already has a "social credit score" and [uses cameras to track individuals](https://www.youtube.com/watch?v=rrFwIShaSd8).  The official guidelines for this score are "To allow the trustworthy to roam everywhere under heaven, while making it hard for the discredited to take a single step".  In the U.S., we are already using financial credit data for life insurance underwriting as a predictor of mortality.  If a similar social credit system were in use today, it would likely be even more predictive of mortality.

**Audio/Text**
- [Patient-doctor conversations](https://bdtechtalks.com/2019/08/27/deep-medicine-ai-doctor-patient-relationship/) can be recorded to automate the medical billing procedure.  Medical codes will become more granular and doctors can spend less time typing on keyboards and more time with the patient, making these conversations more predictive of future health outcomes.  Doctor's notes today suffer from many inconsistencies due in part to how little time doctors spend writing them.  Once better audio-to-text systems are available, this will no longer be an issue.
- Phone recordings from customers can be translated into text and used to assess the customers mood, stress level, or even if they are a smoker by the sound of their voice.  Filing claims will become less expensive as AI staff can take over the claims processing, from answering calls from humans to sending bills by email.  Deductibles and copays, which are partially used to reduce the number of low-cost claims that are filed due to administrative expenses, or LAE, will become less common.

**Sensor Technology**
- The Internet of Things (IoT) refers to sensors that collect data on things such as medical devices, fit bits, home security systems, cars, and mobile devices.  [McKinsey](https://www.mckinsey.com/industries/financial-services/our-insights/digital-ecosystems-for-insurers-opportunities-through-the-internet-of-things) has a report on how the IoT will impact the insurance world in may other examples.
- Electronic Health Records (EHR) will be ubiquitous in 3-5 years.  This data is in an unstructers format that only AI/ML algorithms are capable of dealing with.
- Insurance companies can provide discounts to homeowners that install security systems.  They can then collect this data to learn more about their customers and improve underwriting decisions.
- Assisted living facilities will use devices to improve the quality of care in the aging population.  Insurance comapnies can provide lower premiums in exchange for participating.  
- Commercial lines insurers can use sensor technology to better predict future claims.  Imagine a company that has purchased insurance to cover a shipment of goods from Asia to the US using sensors to track damaged cargo.

## Actuaries will need to become team players

AI is an entire field of study that focuses on how human intelligense is replicated by machines.  Like computer science or economics, this is a vast body of rapidly expanding knowledge, and too much information to add to the actuarial syllabus.  Meanwhile, a new generation is learning this field quickly.  

China provides a good example of where the US will be in several years.  AI was recently added to China's [high-school curriculumn.](https://www.abacusnews.com/digital-life/china-brings-ai-high-school-curriculum/article/2144442).  The country's educational system fully embraces the new technology, going so far as to putting [brain-monitoring](https://www.youtube.com/watch?v=JMLsHI8aV0g) headbands on children in classrooms.  These kids are going to grow up with a deeper understanding of AI than anyone over the age of 20 can hope to acquire in their lifetime.  

The punchline is that actuaries will no longer be the experts at predicting the future.  This knowledge gap represents two challenges:

1. Programming skills required to deal with increasingly complex software.  
2. Non-traditional data sources (Video, Audio, Text, Sensors, etc).

Looking at how the surgical profession has adopted to technology provides insight into how the actuarial industry will.  Traditionally, surgeons would be solely responsible for the patient, from the moment that they where put on the operating table to the post-op discussion with the patient's family.  

They led the way with a scalpel as the actuary leads the way with a spreadsheet.  As medical technology as advanced, we know need anesthesiologists, radiologists, pathologist, and nurses to step up and contribute.  In his book *Complications*, Dr. Atul Gawande, who is now the CEO of Haven Health said that **"Surgery used to be a solo act where the surgeon was the virtuoso, but today, surgery is a team sport because medical technology has become too complex for one person to learn."**

The actuary of the future will be surrounded by a team of data scientists and machine learning engineers in a similar way.

## Model ethics and AI explainability will matter

It will take AI decades to develop the softer human intelligence skills such as empathy and a sense of fairness.  As model inputs come from traditionally "protected" sources, such as facial characteristics, genetic ancestry, social media data, criminal and pre-criminal history (i.e., social credit scores), models will have the capacity to violate human rights.  

Once companies realize that humans are more likely trust (and therefore purchase) their AI products if they understand the user, machine empathy will be in high demand.

> The key to social integration is to master the ability to understand what other people feel and think, and react accordingly. Until now, this capacity has been reserved only for (some) humans. This virtue called empathy improves socialisation, and humans are sociable by nature.

https://towardsdatascience.com/deep-learning-for-machine-empathy-robots-and-humans-interaction-part-i-8142fccd6050

Models that are based on biased or prejudiced data are going to learn and repeat this pattern, or said another way: ["Bias in; bias out"](https://www.bloomberg.com/opinion/articles/2018-10-16/amazon-s-gender-biased-algorithm-is-not-alone). Data science teams will be put under scrutiny by civil rights lawyers to show that their models are non-discriminatory.  In the insurance world, it will fall on the actuaries, who understand the insurance regulation better than the data scientists, to prove to that these models are fair. There could be new actuarial [standards of practice](http://www.actuarialstandardsboard.org/standards-of-practice/) which address this area.

Explainability is the ability to translate the model's reasoning into human language.  This is necessary to determine if a model is biased or not.  For example: suppose that an insurer has an underwriting model that assigns people to a risk class - either ACCEPT or DENY for the sake of simplicity.  One input may be the persons's morgage history, [which has a history of prejudice](https://www.revealnews.org/article/for-people-of-color-banks-are-shutting-the-door-to-homeownership/), and another input may be the patient's social media page, which contains the person's race.   A neural network would learn that "race -> home owndership -> financial risk".  This would result in a racist model, which if used over millions of other people would further reinforce this pattern of discrimination.  
