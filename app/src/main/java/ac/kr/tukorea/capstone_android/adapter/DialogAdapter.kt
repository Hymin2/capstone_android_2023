package ac.kr.tukorea.capstone_android.adapter

import ac.kr.tukorea.capstone_android.R
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class DialogAdapter(private var mList: ArrayList<String>) :RecyclerView.Adapter<DialogAdapter.ViewHolder>(){

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): DialogAdapter.ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.dialog_list_item, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = mList[position]
        holder.item.text = item
    }

    override fun getItemCount(): Int {
        return mList.size
    }

    class ViewHolder(ItemView: View):RecyclerView.ViewHolder(ItemView) {
        val item : TextView = ItemView.findViewById(R.id.dialog_rvItem)
    }
}