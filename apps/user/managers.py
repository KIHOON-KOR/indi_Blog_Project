from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일은 필수 입력값입니다.")
        
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        
        if password:
            user.set_password(password)
        else:
            # 소셜 로그인 유저의 경우 password가 없을 수 있음
            user.set_unusable_password()
            
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, nickname, password, **extra_fields)