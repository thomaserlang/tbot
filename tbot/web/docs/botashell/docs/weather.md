---
id: weather
title: Weather
---

## Lookup city 

Used to set a default lookup city for the command.

`{weather.lookup_city Aarhus}`

Returns an empty string.

## Units

`imperial` for for Fahrenheit.  
`metric` for for Celsius.

Default is `metric`.

`{weather.units metric}`

Returns an empty string.

## Lookup city 

Used to set a default lookup city for the command.

`{weather.lookup_city <city>}`

## Temperature 

`{weather.temp}`   
`{weather.temp_min}`   
`{weather.temp_max}` 

Example response: `23`

## Description

`{weather.description}`

Example response: `light rain`

## City

Name of the city being looked up.

`{weather.city}`

Example response: `Aarhus`

## Wind speed

`{weather.wind_speed}`

Example response: `4.6`