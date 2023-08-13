# let's go my projects 


Примичание! когда deploy на сервер чтоб статика админа не пропало устанавливаем доп библиотеку

``` pip install whitenoise ```

и в ``` settings.py ``` а именно в MIDDLEWARE[ ]
добовляем 
``` whitenoise.middleware.WhiteNoiseMiddleware ```
если что вот ссылка ``` https://whitenoise.readthedocs.io/en/stable/ ```