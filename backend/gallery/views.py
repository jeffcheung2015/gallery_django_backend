# Create your views here.
import jwt
import uuid
from datetime import datetime, timedelta
from functools import reduce
import operator
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from .models import Image, Profile, Tag, Activity
from .serializers import ImageSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from .utils import auth_header_to_user_id
from .forms import UpsertImageForm, UpdateUserForm, UpdateAvatarForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q

@api_view(['POST'])
@permission_classes([])
def upsert_image(req):
    # querydict is immutable
    req_data = req.data.copy()
    print(">>> upsert_image, req_data :", req_data, req.FILES)

    try:
        user_id = auth_header_to_user_id(req.META['HTTP_AUTHORIZATION'])
        api_type = req.data["api_type"]
        print(">>> upsert_image.user_id:", user_id)
        req_data.__setitem__("user",user_id)
        if not api_type == 'delete':
            req_data.setlist("tags", [int(tag_str) for tag_str in req.data.getlist("tags")])
        print(">>> upsert_image.req_data:", req_data)
        user = User.objects.filter(id=user_id)[0]

        if api_type == 'insert': # insert type
            print(">>> upsert_image [[[INSERT]]]")
            is_insert_success = False
            upsert_img_form = UpsertImageForm(req_data, req.FILES)
            print(">>> upsert_image.upsert_img_form:", upsert_img_form)
            if upsert_img_form.is_valid():
                today_activity = Activity.objects.filter(user=user_id).filter(date__date=datetime.today().date())
                if today_activity.exists():
                    today_activity.update(count=today_activity[0].count + 1)
                else:
                    Activity.objects.create(user=user, count=1)
                is_insert_success = True
                upsert_img_form.save()
            else:
                print(">>> upsert_image.upsert_img_form.errors:", upsert_img_form.errors)
            return Response({
                'resp_code': '00000' if is_insert_success else '00011'
            })
        elif api_type == 'delete':
            print(">>> upsert_image [[[DELETE]]]")
            to_be_deleted_img = Image.objects.filter(id=int(req_data["img_id"]))
            is_delete_success = False
            print(">>> upsert_image.to_be_deleted_img.exists:", to_be_deleted_img.exists())
            if to_be_deleted_img.exists():
                to_be_deleted_img[0].delete()
                img_date = datetime.fromtimestamp(int(req_data["created_at"])/1000).date()
                that_day_activity = Activity.objects.filter(date__date=img_date)
                print(">>> upsert_image.that_day_activity.exists:", that_day_activity.exists())
                if that_day_activity.exists():
                    is_delete_success = True
                    if that_day_activity[0].count > 1:
                        print("that_day_activity[0].count-1", that_day_activity[0].count-1)
                        print("that_day_activity[0]", that_day_activity[0])
                        that_day_activity.update(count=that_day_activity[0].count-1)
                    else:
                        that_day_activity.delete()

            return Response({
                'resp_code': '00000' if is_delete_success else '00013'
            })
        else: # 'update'
            print(">>> upsert_image [[[UPDATE]]]")
            is_update_success = False
            to_be_updated_img = Image.objects.filter(id=int(req_data["img_id"]))
            print(">>> upsert_image.to_be_updated_img:", to_be_updated_img)
            upsert_img_form = UpsertImageForm(req_data, instance=to_be_updated_img[0])
            print(">>> upsert_image.upsert_img_form:", upsert_img_form)
            if upsert_img_form.is_valid():
                upsert_img_form.save()
                is_update_success = True
            else:
                print(">>> upsert_image.upsert_img_form.errors:", upsert_img_form.errors)
            return Response({
                'resp_code': '00000' if is_update_success else '00011'
            })
    except Exception as e:
        print("Exception happens. ", e)
        return Response({
            'resp_code': '99999'
        })


@api_view(['POST'])
@permission_classes([])
def update_avatar(req):
    req_data = req.data.copy()
    print(">>> update_avatar, req_data :", req_data, ",req.FILES: ", req.FILES)
    try:
        user_id = auth_header_to_user_id(req.META['HTTP_AUTHORIZATION'])
        print(">>> update_avatar.user_id:", user_id)
        req_data.__setitem__("last_edit",datetime.now())
        print(">>> update_avatar.req_data:", req_data)
        profile = Profile.objects.filter(user=user_id)[0]
        print(">>> update_avatar.profile: ", profile)
        update_avatar_form = UpdateAvatarForm(req_data, req.FILES, instance=profile)
        print(">>> update_avatar.update_avatar_form: ", update_avatar_form)
        if update_avatar_form.is_valid():
            update_avatar_form.save()
            return Response({
                'resp_code': '00000'
            })
        else:
            print(">>> update_avatar, some form inputs are invalid")
            return Response({
                'resp_code': '99999'
            })
    except Exception as e:
        print("Exception happens. ", e)
        return Response({
            'resp_code': '99999'
        })

@api_view(['POST'])
@permission_classes([])
def update_user(req):
    req_data = req.data.copy()
    print(">>> update_user, req_data :", req_data)
    try:
        user_id = auth_header_to_user_id(req.META['HTTP_AUTHORIZATION'])
        print(">>> update_user.user_id:", user_id)
        req_data.__setitem__("user",user_id)
        req_data.__setitem__("last_edit",datetime.now().date())
        user = User.objects.filter(id=user_id)[0]
        update_user_form = UpdateUserForm(req_data, instance=user)
        profile = Profile.objects.filter(user=user_id)
        if profile.exists():
            profile.update(last_edit=datetime.now())
        # validate_email will throw error if it is invalid email
        validate_email(update_user_form['email'].data)
        isValidPassword = len(update_user_form['password'].data) >= 8
        if update_user_form.is_valid() and isValidPassword:
            # check the uniqueness of the email
            modified_email = update_user_form['email'].data
            print(">>> update_user.modified_email:", modified_email)
            email_to_user = User.objects.filter(email=modified_email)
            if not email_to_user.exists():
                update_user_form.save()
                return Response({
                    'resp_code': '00000'
                })
            else:
                return Response({
                    'resp_code': '00002'
                })
        else:
            print(">>> update_user, some form inputs are invalid")
            return Response({
                'resp_code': '99999'
            })
    except ValidationError:
        print("Email is invalid. ")
        return Response({
            'resp_code': '00007'
        })
    except Exception as e:
        print("Exception happens. ", e)
        return Response({
            'resp_code': '99999'
        })



@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_image(req):
    data = []
    curr_page = 0
    image = None
    # get request data
    print(">>> get_image, req.GET:", req.GET)
    try:
        print(">>> get_image, req.GET:", req.GET.get('page'))
        if req.GET.getlist("tags"):
            print(">>> get_image, req.GET.get('tags')", req.GET.getlist("tags"))
            tags = req.GET.getlist("tags")
            tags_query = Image.objects.filter(tags=int(tags[0]))
            for i in range(1, len(tags)):
                tags_query = tags_query.filter(tags=int(tags[i]))
            images = tags_query.distinct().order_by("created_at")
        else:
            images = Image.objects.all().order_by("created_at")

        page = req.GET.get("page")
        img_per_page = req.GET.get("imgPerPage")
        user_id = req.GET.get("userId")
        paginator = Paginator(images, int(img_per_page))
        data = paginator.page(page)
        curr_page = page
    except PageNotAnInteger:
        data = paginator.page(1)
        curr_page = 1
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
        curr_page = paginator.num_pages
    except Exception as e:
        print("Exception happens. ", e)
        return Response({
            'resp_code': "99999"
        })

    img_serializer = ImageSerializer(data, many=True)
    print(">>> get_image", img_serializer.data)
    return Response({
        'resp_code': '00000',
        'data': img_serializer.data,
        'img_count': paginator.count,
        'num_pages': paginator.num_pages,
        'curr_page': int(curr_page)
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_tags(req):
    print(">>> get_tags, req.GET:", req.data)
    try:
        tags = Tag.objects.all()
        print(">>> get_tags, tags:", tags)
        return Response({
            'resp_code': '00000',
            'tags': [tag.tag_name for tag in tags]
        })
    except Exception as e:
        print("Exception happens. ", e)
        return Response({
            'resp_code': "99999"
        })



@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def user_signup(req):
    req_data = req.data
    print(">>> user_signup, req_data :", req_data)

    username, password, email = '', '', ''
    try:
        username = req_data['username']
        password = req_data['password']
        email = req_data['email']

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return Response({
                'resp_code': '00002'
            })
        elif len(password) < 8:
            return Response({
                'resp_code': '00006'
            })
        validate_email(email)
        created_user = User.objects.create_user(username, email, password)
        profile = Profile.objects.create(user=created_user)
        return Response({
            'resp_code': '00000'
        })

    except ValidationError:
        print("Email is invalid. ")
        return Response({
            'resp_code': '00007'
        })
    except KeyError:
        return Response({
            'resp_code': '00001'
        })
    except Exception as e:
        print("Exception happens. ", e)
        return Response({
            'resp_code': '99999'
        })



@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def user_login(req):
    req_data = req.data
    print(">>> user_login, req_data:", req_data)

    username, password = '', ''
    try:
        username = req_data['username']
        password = req_data['password']
    except KeyError:
        return Response({
            'resp_code': '00001'
        })
    except Exception as e:
        print("Exception happens. ", e)
        return Response({
            'resp_code': '99999'
        })
    if not User.objects.filter(username=username).exists():
        return Response({
            'resp_code': '00003'
        })
    else:
        try:
            user = authenticate(username=username, password=password)
            profile = Profile.objects.filter(user=user.id)[0]
            print(profile)
            login(req, user)
            # have the 00000 resp_code inserted
            refresh = RefreshToken.for_user(user)
            print(refresh)
            return Response({
                'resp_code': "00000",
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'email': user.email,
                'date_joined': user.date_joined,
                'last_login': user.last_login,

                'avatar': profile.avatar.url,
                'last_edit': profile.last_edit,
            })
        except Exception as e:
            print("Exception happens. ", e)
            return Response({
                'resp_code': '00004'
            })


@api_view(['GET', 'POST'])
@permission_classes([])
def user_logout(req):
    print(">>> user_logout:")
    logout(req)
    return Response({
        'resp_code': '00000'
    })



@api_view(['POST'])
@permission_classes([])
def get_user(req):
    print(">>> get_user.req.data: ", req.data)
    req_data = req.data

    try:
        auth_header_str = req.META['HTTP_AUTHORIZATION']
        access_token = auth_header_str.split()[1]
        decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        print(">>> get_user.decoded_token: ", decoded_token)
        user_id = decoded_token["user_id"]

        user = User.objects.get(id=int(user_id))
        print(">>> get_user.user:", user)
        profile = Profile.objects.filter(user=user_id)[0]
        print(">>> get_user.profile:",dir(profile.avatar))
        no_of_imgs = Image.objects.filter(user=user_id).count()
        curr_user_activity = []
        lower_limit = datetime.today().date() - timedelta(days=91)
        filter_query = Activity.objects.filter(user=user_id).filter(date__date__gte=lower_limit)
        if filter_query.exists():
            for activity in filter_query:
                curr_user_activity += [(activity.date.date(), activity.count)]
        return Response({
            'resp_code': '00000',
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined,
            'last_login': user.last_login,

            'avatar': profile.avatar.url,
            'last_edit': profile.last_edit,
            'no_of_imgs': no_of_imgs,
            'activity': curr_user_activity
        })
    except KeyError:
        return Response({
            'resp_code': '00005'
        })
    except (User.DoesNotExist, Profile.DoesNotExist) as e:
        console.log(">>> get_user, error=", e)
        return Response({
            'resp_code': '00003'
        })
    except Exception as e:
        print("Exception happens. ", e)
        return Response({
            'resp_code': '99999'
        })
