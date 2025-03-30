from django.core.mail.backends.smtp import EmailBackend
import smtplib
import ssl



class CustomEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False

        try:
            # Создаем соединение с SMTP-сервером
            self.connection = self.connection_class(
                host=self.host,
                port=self.port,
                local_hostname=None,
                timeout=self.timeout,
                source_address=None,
            )

            # Если используется TLS, настраиваем его
            if not self.use_ssl and self.use_tls:
                context = ssl._create_unverified_context()  # Отключаем проверку сертификата
                self.connection.starttls(context=context)

            # Если указаны логин и пароль, выполняем аутентификацию
            if self.username and self.password:
                self.connection.login(self.username, self.password)

            return True
        except Exception:
            if not self.fail_silently:
                raise


# class CustomEmailBackend(EmailBackend):
#     def open(self):
#         if self.connection:
#             return False
#         try:
#             self.connection = smtplib.SMTP_SSL(self.host, self.port, context=ssl.create_default_context())
#             self.connection.login(self.username, self.password)
#         except Exception as e:
#             print(f"Error: {e}")
#             raise
#         return True