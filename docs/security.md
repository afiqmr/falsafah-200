# Security and privacy

## What is public

- This repository and the built app are public. The Firebase web config in
  `cloud/firebase-config.json` is public by design: it only identifies the project. Access is
  controlled by the Firestore rules below.
- The admin email appears in `cloud/cloud_ui.html` (`ADMIN_EMAILS`) and in the rules. The two
  must match.

## What is not public

- **Student progress**: each student can read and write only their own `users/{uid}` document.
- **Dr. HALO-N's recordings**: only signed-in students can read them, from `stats/halon-*`. They
  are uploaded through the admin panel and must never be committed to this repository.
- **PINs**: stored only by Firebase Auth as the account password. The app never saves them.

## Firestore rules

Project `falsafah-200-test`:

```text
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    function isAdmin() {
      return request.auth != null
        && request.auth.token.email == 'afiqmonsieur@gmail.com'
        && request.auth.token.email_verified == true;
    }
    match /users/{uid} {
      allow read, write: if request.auth != null && request.auth.uid == uid;
      allow read: if isAdmin();
    }
    match /usernames/{name} {
      allow get: if true;
      allow list, update, delete: if false;
      allow create: if request.auth != null
        && name.matches('^[a-z0-9_.]{3,20}$')
        && request.resource.data.keys().hasOnly(['uid', 'email'])
        && request.resource.data.uid == request.auth.uid
        && request.resource.data.email == request.auth.token.email;
    }
    match /stats/{doc} {
      allow read: if request.auth != null;
      allow write: if isAdmin();
    }
  }
}
```

`usernames` allows a single `get` without signing in, because the login screen needs the email
behind a username. Listing the collection is blocked, so usernames cannot be enumerated.

## Admin role

The account registered with the admin email, after verifying it, gets **Papan pentadbir** in the
account sheet. It lists every student's progress, publishes the weekly class list, and uploads
recordings. To change the admin, change the email in both `ADMIN_EMAILS` and the rules.

## Third parties

| Service                     | Receives                                                |
| --------------------------- | ------------------------------------------------------- |
| Firebase (Google)           | Account email, username, name and study progress        |
| Quran.com                   | Requests for verse words and audio (no student data)    |
| Google Fonts                | Font requests                                           |
| Google or Apple speech      | The student's voice, only while the voice check listens |
| Vercel                      | Standard web request logs                               |

The app has no analytics or tracking. The voice check tells students it checks words only; the
recording itself is handled by the phone's speech service, not by this app.

## Rules for contributors

- Never commit secrets, service-account keys, recordings or real student data.
- Use demo accounts and demo progress in screenshots and videos.
- The share card and share text never include the Catitan.
