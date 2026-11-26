---
title: "Olfactory Maps!"
summary: "Mapping the smells of a city — bakeries, florists, parks — with Folium and the Google Places API."
date: 2024-01-23
image: /img/stamen_toner_map.png
tags: [maps, Folium, Python]
wip: true
---

![Smell map of a neighbourhood](/img/stamen_toner_map.png)


Describing the layout of smells in a city with Folium and Google Places API. I've always wanted to attempt to visualize or represent the experience of walking through a city, entering and exiting different olfactory zones like coffee shops and especially bakeries. In particular, I think of the Mt Pleasant neighborhood in Vancouver where there are a few bakeshops and I'm not sure if it's still there, but a Terra Breads factory and how the smell of something delicious would waft whenever passing by those few blocks. You smell it before you even realize where exactly the factory is. 

This is my current best and pretty lame attempt at representing this information. It would be cool to add a wind direction API to this as well. In the short term, just some map navigation and map center update code is the priority. 

- Toast = Bakeries
- Pink = Florists
- Green = Parks


<figure class="chart">
  <iframe src="/charts/map_stadia_stamen_toner.html" title="Bakeries, florists and parks on a toner map" loading="lazy"></iframe>
</figure>


