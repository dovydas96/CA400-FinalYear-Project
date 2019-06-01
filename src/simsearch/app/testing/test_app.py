import io
from app import routes


def test_main_page(client):
    """Test if landing page is up"""

    response = client.get('/login', follow_redirects=True)
    assert response.status_code == 200


def test_register_page(client):
    """Test if users can access register page"""

    response = client.get('/register', follow_redirects=True)
    assert response.status_code == 200


def test_unregistered_user_access(client):
    """Test if users can access page they should not be able to access
     without logging in"""

    response = client.get('/upload/test', follow_redirects=True)
    assert b'Please log in to access this page.' in response.data


def test_valid_user_registration(client):
    """Test a user can register for the app"""

    response = register(client, 'testy', 'testyy@test.com', 'testing', 'testing')
    assert response.status_code == 200
    assert b'Congratulations, you are now a registered user!' in response.data


def test_valid_user_duplicate_user(client):
    """Test a user cannot create an account with duplicate username or email"""

    response = register(client, 'testy', 'testyy@test.com', 'testing', 'testing')
    assert response.status_code == 200
    response = register(client, 'testy', 'testyy@test.com', 'testing', 'testing')
    assert b'Please use a different username.' in response.data
    assert b'Please use a different email address.' in response.data


def test_invalid_user_registration_different_passwords(client):
    """Test if user cannot register with different passwords"""

    response = register(client, 'testy', 'test@test.com', 'test', 'testy')
    assert b'Field must be equal to password.' in response.data


def test_invalid_login(client):
    """Make sure user cannot login with false credentials"""

    response = login(client, "xxx", "xxx", redirect=True)
    assert b'Invalid username or password' in response.data


def test_login(client):
    """Test if user can login and get redirected to upload page"""

    response = login(client, "test", "test", redirect=False)
    assert response.status_code == 302


def test_logout(client):
    """Test if user can logout"""

    response = login(client, "test", "test", redirect=True)
    assert response.status_code == 200
    response = logout(client)
    assert response.status_code == 200


def test_logged_in_access(client):
    """Test if logged in user can view pages logged in users can"""

    response = login(client, "test", "test", redirect=False)
    assert response.status_code == 302
    response = client.get('/upload/test', follow_redirects=True)
    assert response.status_code == 200
    response = client.get('/user/test', follow_redirects=True)
    assert response.status_code == 200


def test_file_upload(client):
    """Test if user can upload photo."""

    response = login(client, "test", "test", redirect=False)
    assert response.status_code == 302
    files = 'app/testing/test.jpeg'
    response = upload_image(client, files, redirect=True)
    assert response.status_code == 200


def test_incorrect_file_upload(client):
    """Test if users are not allowed to upload incorrect file types"""

    response = login(client, "test", "test", redirect=False)
    assert response.status_code == 302
    file = (io.BytesIO(b'my file contents'), "test.test")
    response = upload_image(client, file, redirect=True)
    assert b"Incompatible File" in response.data


def test_previous_queries(client):
    """Test if the uploaded file is in the database"""

    response = login(client, "test", "test", redirect=True)
    assert response.status_code == 200
    files = 'app/testing/test.jpeg'
    response = upload_image(client, files, redirect=True)
    assert response.status_code == 200
    response = client.get('/user/test', follow_redirects=True)
    assert b"test.jpeg" in response.data


def test_search_previous(client):
    """Test if searching for previously uploaded image is working"""

    response = login(client, "test", "test", redirect=False)
    assert response.status_code == 302
    file = "test/test.jpeg"
    response = search_image(client, file)
    assert response.status_code == 200


def test_delete_file(client):
    """Test if file is deleted """
    response = login(client, "test", "test", redirect=False)
    assert response.status_code == 302
    bucket = routes.get_bucket()
    key = "test/temp.png"
    response = delete_image(client, key)
    bucket.Object(key).delete()
    assert b"Successfully removed file" in response.data


def test_rating_system(client):
    """Test if rating system is working"""

    response = login(client, "test", "test", redirect=True)
    assert response.status_code == 200
    query = "test.jpeg, img/MEN/Denim/id_00000080/01_1_front.jpg, positive"
    response = rating_check(client, query)
    assert b'Thank you for your feedback!' in response.data


def test_delete_account(client):
    """Test if user can delete accounts"""
    logout(client)
    response = login(client, "testyy", "testyy", redirect=True)
    assert response.status_code == 200
    response = delete_account(client)
    assert response.status_code == 200
    response = login(client, 'testyy', 'testyy', redirect=True)
    assert b'Invalid username or password' in response.data


def rating_check(client, query):
    return client.get('/ratings', data=dict(key=query),
                      content_type='multipart/form-data',
                      follow_redirects=True)


def delete_account(client):
    return client.get(
        '/delete_account',
        follow_redirects=True
    )


def search_image(client, file):
    return client.post(
        '/search_previous',
        data=dict(key=file),
        content_type='multipart/form-data',
        follow_redirects=True
    )


def delete_image(client, file):
    return client.post(
        '/delete',
        data=dict(key=file),
        content_type='multipart/form-data',
        follow_redirects=True
    )


def upload_image(client, file, redirect):
    return client.post(
        '/upload/test',
        data=dict(photo=file),
        content_type='multipart/form-data',
        follow_redirects=redirect
    )


def register(client, username, email, password, confirm):
    return client.post(
        '/register',
        data=dict(username=username, email=email, password=password, password2=confirm),
        follow_redirects=True
    )


def login(client, username, password, redirect):
    return client.post(
        '/',
        data=dict(username=username, password=password),
        follow_redirects=redirect
    )


def logout(client):
    return client.get(
        '/logout',
        follow_redirects=True
    )
