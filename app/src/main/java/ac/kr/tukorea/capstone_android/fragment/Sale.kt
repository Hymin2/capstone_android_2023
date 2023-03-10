package ac.kr.tukorea.capstone_android.fragment

import ac.kr.tukorea.capstone_android.adapter.SaleAdapter
import ac.kr.tukorea.capstone_android.data.Products
import ac.kr.tukorea.capstone_android.R
import ac.kr.tukorea.capstone_android.activity.SaleActivity
import ac.kr.tukorea.capstone_android.activity.WriteActivity
import android.content.Intent
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.floatingactionbutton.FloatingActionButton
import kotlin.collections.ArrayList

// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val ARG_PARAM1 = "param1"
private const val ARG_PARAM2 = "param2"

/**
 * A simple [Fragment] subclass.
 * Use the [Home.newInstance] factory method to
 * create an instance of this fragment.
 */
class Home : Fragment() {
    // TODO: Rename and change types of parameters
    private var param1: String? = null
    private var param2: String? = null

    private lateinit var adapter : SaleAdapter
    private lateinit var recyclerView : RecyclerView
    private lateinit var productsArrayList : ArrayList<Products>
    private lateinit var writeFAB : FloatingActionButton

    lateinit var imageId : Array<Int>
    lateinit var title : Array<String>
    lateinit var price : Array<Int>
    lateinit var content : Array<String>


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        arguments?.let {
            param1 = it.getString(ARG_PARAM1)
            param2 = it.getString(ARG_PARAM2)
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_home, container, false)
    }

    companion object {
        /**
         * Use this factory method to create a new instance of
         * this fragment using the provided parameters.
         *
         * @param param1 Parameter 1.
         * @param param2 Parameter 2.
         * @return A new instance of fragment Home.
         */
        // TODO: Rename and change types and number of parameters
        @JvmStatic
        fun newInstance(param1: String, param2: String) =
            Home().apply {
                arguments = Bundle().apply {
                    putString(ARG_PARAM1, param1)
                    putString(ARG_PARAM2, param2)
                }
            }
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        dataInitialize()
        val layoutManager = LinearLayoutManager(context)
        recyclerView = view.findViewById(R.id.sale_recycler_view)
        recyclerView.layoutManager = layoutManager
        recyclerView.setHasFixedSize(true)
        adapter = SaleAdapter(productsArrayList)
        recyclerView.adapter = adapter
        writeFAB = view.findViewById(R.id.write_fab)

        writeFAB.setOnClickListener{
            val intent = Intent(getActivity(), WriteActivity::class.java)
            startActivity(intent)
        }

        getUserData()
    }


    private fun dataInitialize() {

        productsArrayList = arrayListOf<Products>()

        imageId = arrayOf(
            R.drawable.galaxys23,
            R.drawable.iphone14pro,
        )

        title = arrayOf(
            "????????? S23 ???????????????",
            "????????? 14?????? ???",
        )

        price = arrayOf(
            1000000,
            1100000,
        )

        content = arrayOf(
            "512?????? ????????????\n" +
                    "S23 ?????????\n" +
                    "???????????? ?????????\n" +
                    "?????????????????? ?????? ?????? ??? ????????????\n" +
                    "?????????????????? ????????? ?????? ????????????",
            "????????? ?????????2",
        )
    }

    private fun getUserData() {
        for (i in imageId.indices) {
            val products = Products(imageId[i], title[i], price[i])
            productsArrayList.add(products)
        }

        var adapter = SaleAdapter(productsArrayList)
        recyclerView.adapter = adapter
        adapter.setOnItemClickListener(object : SaleAdapter.onItemClickListener{
            override fun onItemClick(position: Int) {

                val intent = Intent(context,SaleActivity::class.java)
                intent.putExtra("title",productsArrayList[position].saleTitle)
                intent.putExtra("imageId",productsArrayList[position].saleImage)
                intent.putExtra("price",productsArrayList[position].salePrice)
                intent.putExtra("content",content[position])

                startActivity(intent)
            }
        })
    }
}