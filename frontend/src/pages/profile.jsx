import { useEffect, useState } from "react";
import api from "../api/axios";

function Profile() {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    getProfile();
  }, []);

  const getProfile = async () => {
    try {
      const response =
        await api.get("/auth/profile");

      setProfile(
        response.data.user ||
          response.data
      );
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>My Profile</h1>

      <div className="profile-card">
        <div className="profile-avatar">
          👤
        </div>

        <h2>
          {profile?.name || "User"}
        </h2>

        <p>
          {profile?.email || ""}
        </p>

        {profile?.id && (
          <p>
            User ID: {profile.id}
          </p>
        )}
      </div>
    </div>
  );
}

export default Profile;