package ac.kr.tukorea.capstone_android.data

import com.google.gson.annotations.SerializedName

data class ChatRoomResponseBody(
    @SerializedName("result")
    val result : String,
    @SerializedName("status")
    val status: String,
    @SerializedName("message")
    val message : ChatRoom
)