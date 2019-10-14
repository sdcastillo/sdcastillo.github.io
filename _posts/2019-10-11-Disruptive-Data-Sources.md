---
title: "Disruptive Data Sources"
layout: post
excerpt: ""
categories:
  - AI
  - Insurance
  - Data
tags:
last_modified_at: 2019-10-11T12:43:31-05:00
---

Innovations begin when new information is made available.  Deep learning can use data that no other algorithms can.  Video, audio, text, and sensor data such as electronic health records can now be used in models to predict future events.

A few of the applications are:

**Video**

Deep learning can interpret objects from videos.  One example is [Densely Annotated VIdeo Segmentation (DAVIS)](https://davischallenge.org/index.html), which identifies objects (cars, people, birds, etc) from videos. 

<iframe width="560" height="315" src="https://www.youtube.com/embed/8f9y17-OAwI?start=26" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen> </iframe>


Methods such as DAVIS can be used for:

- Using vehicle video and sensor data to assess risk in auto insurance.  Drivers that exhibit riskier behavior can be identified *before* they get into accidents, and safe drivers can be rewarded.  By 2030-2035, when self-driving cars are commonplace, vehicles will collect [terabytes of data per year](https://www.tuxera.com/blog/autonomous-cars-300-tb-of-data-per-year/).
- Installing [surveillance cameras](https://en.wikipedia.org/wiki/Artificial_intelligence_for_video_surveillance) around buildings to measure foot traffic, fire and vandalism risk, customer engagement, and other factors.  For example, if there are more people walking in and out of the store, it is more likely that a person will fall, injure themselves, and sue the retailer. 
- Facial recognition cameras that record time and location of individuals.  There are many potential use cases for this.  [China](https://time.com/collection/davos-2019/5502592/china-social-credit-score/) already has a "social credit score" and [uses cameras to track individuals](https://www.youtube.com/watch?v=rrFwIShaSd8).  The official guidelines for this score are "To allow the trustworthy to roam everywhere under heaven, while making it hard for the discredited to take a single step".  In the U.S., we are already using financial credit data for life insurance underwriting as a predictor of mortality.  If a similar social credit system were in use today, it would likely be even more predictive of mortality.

**Audio & Text**

Audio is really a series of waves, and waves can be translated into time series, which can be fed into a model.  Feeding sound along with labels (i.e., subtitles) into a model allows for the sound to be translated into words.

<iframe width="560" height="315" src="https://www.youtube.com/embed/Qf4YJcHXtcY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

The are *many* use cases for audio/text translation.  With regard to insurance, two common areas are

- In hospitals and medical offices, [patient-doctor conversations](https://bdtechtalks.com/2019/08/27/deep-medicine-ai-doctor-patient-relationship/) can be recorded to automate the medical billing procedure.  Medical codes will become more granular and doctors can spend less time typing on keyboards and more time with the patient, making these conversations more predictive of future health outcomes.  Doctor's notes today suffer from many inconsistencies due in part to how little time doctors spend writing them.  Once better audio-to-text systems are available, this will no longer be an issue.  Google is already using deep learning to [remotely treat diabetes patients](https://intouchhealth.com/how-ai-augments-telehealth/).

- Phone recordings from customers can be translated into text and used to assess the customers mood, stress level, or even if they are a smoker by the sound of their voice.  Filing claims will become less expensive as AI staff can take over the claims processing, from answering calls from humans to sending bills by email.  Deductibles and copays, which are partially used to reduce the number of low-cost claims that are filed due to administrative expenses, or LAE, will become less common.  The startup Lemonade already [uses chatbots for claims processing](https://stories.lemonade.com/lemonade-sets-new-world-record-706ef8674110).

- Text from claim notes can be used in models.  In P&C insurance coverages where lawsuits can drive up claim costs, police reports, witness statements, adjustor notes, or recorded statements can contain valuable insights that were previously unusable.  The firm [Megaputer](https://www.megaputer.com/wp-content/uploads/insurance-subrogation-prediction-case-study.pdf) already offers this as a product, and this is not a new idea; however, [2019 saw several breakthroughs in NLP](https://www.zdnet.com/article/the-state-of-ai-in-2019-breakthroughs-in-machine-learning-natural-language-processing-games-and-knowledge-graphs/).  Google's BERT and Transformer, Allen Instituge's ELMo, OpenAI's Transfomer, Ruder and Howard's ULMFiT, and Microsoft's MT-DNN demonstrated that pre-trained models can substantially improve on many NLP tasks.  

**Sensor Technology**

This is the broadest category, and will eventually have the most impact.  The [Internet of Things (IoT)](https://towardsdatascience.com/iot-machine-learning-is-going-to-change-the-world-7c4e0cd7ac32) refers to sensors that collect data on things such as medical devices, fit bits, home security systems, cars, and mobile devices.  [McKinsey](https://www.mckinsey.com/industries/financial-services/our-insights/digital-ecosystems-for-insurers-opportunities-through-the-internet-of-things) has a report on how the IoT will impact the insurance world in many other examples.

- Using aerial drones for monitoring construction sites for building hazards or [monitoring crops for predicting future yields](https://www.aerobotics.com/?identifier=default-get-in-touch-button).
- Health insurers will provide discounts for those who provide personal data.  In addition to Electronic Health Records (EHR) becoming ubiquitous in the next 3-5 years, wearables such as heart rate monitors, smart watches, step counters, and other medical sensors will be connected to the internet.   
- Do you want to buy pet insurance for your dog?  Just put a GPS tracker on their coller that will record their health, risk of getting hit by a car, and activity level in a similar way to how [AI helping farmers track cow's health].(https://www.blog.google/technology/ai/using-tensorflow-keep-farmers-happy-and-cows-healthy/)
- Assisted living facilities will use devices to improve the quality of care in the aging population.  Insurance companies can provide lower premiums in exchange for participating.  

These three areas of Video, Audio, and Sensor Technology are going to change the world of risk assessment.  In the previous post, we covered [technologies that actuaries are excited about](http://artificialactuary.com/ai/actuarial%20science/2019/09/28/New-Technology.html) and AI was at the top of the list.  

Are there items that have not been included?  Leave a comment below.


