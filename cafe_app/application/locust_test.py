import datetime
import json
import time
import random
import json
import string
from locust import HttpUser, task, tag, between, constant_throughput


# Статичные данные для тестирования
CLIENT_NAMES = ['aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff', 'ggg', 'hhh']
PRODUCT_NAMES = ['aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh']
CLIENT_EMAILS = ['aaa@mail.ru', 'bbb@mail.ru', 'ccc@mail.ru', 'ddd@mail.ru',
                 'eee@mail.ru', 'fff@mail.ru', 'ggg@mail.ru', 'hhh@mail.ru']

PAYMENT_TYPES = ['SberPay', 'GooglePay', 'Card', 'QR-code']


class RESTServerUser(HttpUser):
    """ Класс, эмулирующий пользователя / клиента сервера """
    wait_time = constant_throughput(0.05)

    def on_start(self):
        self.client.get("/api/zoo_cafe/payment_type")    # дефолтная страница - получение списка всех вариантов оплаты

    @tag("get_all_task")
    @task(3)
    def get_all_task(self):
        """ Тест GET-запроса (получение всех записей о продуктах) """
        with self.client.get(f'/api/zoo_cafe/product',
                             catch_response=True,
                             name='/api/zoo_cafe/product') as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f'Status code is {response.status_code}')


    @tag("get_one_task")
    @task(5)
    def get_one_task(self):
        """ Тест GET-запроса (получение одной записи) """
        product_id = random.randint(0, 7)
        product_name = PRODUCT_NAMES[product_id]
        with self.client.get(f'/api/zoo_cafe/product/{product_name}',
                             catch_response=True,
                             name=f'/api/zoo_cafe/product/{product_name}') as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f'Status code is {response.status_code}')


    # @tag("put_task")
    # @task(3)
    # def put_task(self):
    #     """ Тест PUT-запроса (обновление записи о продукте) """
    #     product_id = random.randint(0, 7)
    #     product_name = PRODUCT_NAMES[product_id]
    #
    #     test_data = {'product_name': product_name,
    #                  'description': product_name + " description",
    #                  'quantity_in_stock': random.randint(1000, 2000),
    #                  'prime_cost': str(random.uniform(0.01, 5.99)),
    #                  'final_cost': str(random.uniform(0.01, 5.99))}
    #
    #     put_data = json.dumps(test_data)
    #
    #     with self.client.put('/api/zoo_cafe/product',
    #                          catch_response=True,
    #                          name='/api/zoo_cafe/product',
    #                          data=put_data,
    #                          headers={'content-type': 'application/json'}) as response:
    #         if response.status_code == 202:
    #             response.success()
    #         else:
    #             response.failure(f'Status code is {response.status_code}')

    @tag("put_task")
    @task(1)
    def put_task(self):
        """ Тест PUT-запроса (обновление личных данных пользователя) """
        client_id = random.randint(0, 7)
        client_name = CLIENT_NAMES[client_id]
        client_email = CLIENT_EMAILS[client_id]
        # letters = string.ascii_lowercase
        # rand_name = ''.join(random.choice(letters) for i in range(15))

        test_data = {'customer_name': client_name,
                     'email': client_email}

        put_data = json.dumps(test_data)

        with self.client.put('/api/zoo_cafe/customer',
                             catch_response=True,
                             name='/api/zoo_cafe/customer',
                             data=put_data,
                             headers={'content-type': 'application/json'}) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f'Status code is {response.status_code}')

    @tag("post_task")
    @task(1)
    def post_task(self):
        payment_type_id = random.randint(0, 3)
        payment_type = PAYMENT_TYPES[payment_type_id]

        client_id = random.randint(0, 7)
        client_name = CLIENT_NAMES[client_id]

        num_products = random.randint(1, 5)
        products_in_order = []
        for i in range(num_products):
            product_id = random.randint(0, 7)
            product_name = PRODUCT_NAMES[product_id]
            products_in_order.append(product_name)

        """ Тест POST-запроса (создание записи о заказе) """
        test_data = {'customer': client_name,
                     'products': products_in_order,
                     'date_time': f'{datetime.datetime.now()}',
                     'payment_type': payment_type}
        post_data = json.dumps(test_data)

        with self.client.post('/api/zoo_cafe/order',
                              catch_response=True,
                              name='/api/zoo_cafe/order', data=post_data,
                              headers={'content-type': 'application/json'}) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f'Status code is {response.status_code}')