package ac.kr.tukorea.capstone_android.adapter

import ac.kr.tukorea.capstone_android.activity.DetailActivity
import androidx.fragment.app.Fragment
import androidx.viewpager2.adapter.FragmentStateAdapter

class GraphTabAdapter(fragmentActivity: DetailActivity) : FragmentStateAdapter(fragmentActivity) {
    var fragments: ArrayList<Fragment> = ArrayList()

    override fun getItemCount(): Int {
        return fragments.size
    }

    override fun createFragment(position: Int): Fragment {
        return fragments[position]
    }

    fun addFragment(fragment: Fragment) {
        fragments.add(fragment)
        notifyItemInserted(fragments.size - 1)
    }

    fun removeFragement() {
        fragments.removeLast()
        notifyItemRemoved(fragments.size)
    }
}