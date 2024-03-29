package ac.kr.tukorea.capstone_android.retrofit

import ac.kr.tukorea.capstone_android.API.RetrofitAPI
import ac.kr.tukorea.capstone_android.activity.DetailActivity
import ac.kr.tukorea.capstone_android.adapter.ProductAdapter
import ac.kr.tukorea.capstone_android.adapter.ProductDetailsAdapter
import ac.kr.tukorea.capstone_android.adapter.RecommendProductAdapter
import ac.kr.tukorea.capstone_android.adapter.TopItemAdapter
import ac.kr.tukorea.capstone_android.data.ProductDetails
import ac.kr.tukorea.capstone_android.data.ProductDetailsResponseBody
import ac.kr.tukorea.capstone_android.data.ProductList
import ac.kr.tukorea.capstone_android.data.ProductListResponseBody
import ac.kr.tukorea.capstone_android.databinding.ActivityDetailBinding
import ac.kr.tukorea.capstone_android.databinding.FragmentMainBinding
import ac.kr.tukorea.capstone_android.fragment.Main
import ac.kr.tukorea.capstone_android.util.App
import android.content.Intent
import android.os.Build
import android.util.Log
import androidx.annotation.RequiresApi
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response


class RetrofitProduct{
    private val service = RetrofitAPI.productService

    fun getProductList(name : String?, filter : String?, category: Long, binding: FragmentMainBinding, fragment: Main) {
            service.getProductList(token = App.prefs.getString("access_token", ""), name, filter, category).enqueue(object: Callback<ProductListResponseBody>{
                @RequiresApi(Build.VERSION_CODES.N)
                override fun onResponse(
                    call: Call<ProductListResponseBody>,
                    response: Response<ProductListResponseBody>,
                ) {
                    if(response.isSuccessful){
                        val arrayList : ArrayList<ProductList> = response.body()!!.message.productList as ArrayList<ProductList>
                        val adapter = ProductAdapter(arrayList, binding.root.context)

                        binding.apply {

                            productRecyclerView.adapter = adapter
                            productRecyclerView.addOnScrollListener(object : RecyclerView.OnScrollListener(){
                                override fun onScrolled(recyclerView: RecyclerView, dx: Int, dy: Int) {
                                    super.onScrolled(recyclerView, dx, dy)
                                }
                            })

                            adapter.setOnItemClickListener(object : ProductAdapter.onItemClickListener{
                                override fun onItemClick(position: Int) {
                                    var intent = Intent(binding.root.context, DetailActivity::class.java)
                                    var item = adapter.getItem(position)

                                    intent.putExtra("productId", item.id)
                                    intent.putExtra("productName", item.productName)
                                    intent.putExtra("productPath", item.images[0])
                                    /*
                                    val graphWeekFragment = graphWeek()
                                    var bundle = Bundle()
                                    bundle.putLong("productId", item.id)
                                    val id = item.id
                                    Log.e("보내는 아이디","$id")
                                    graphWeekFragment.arguments = bundle
                                    */

                                    fragment.startActivity(intent)
                                }
                            })
                        }


                    }else{
                        val retrofitRefresh = RetrofitRefresh()
                        retrofitRefresh.refreshToken()

                        getProductList(name, filter, category, binding, fragment)
                    }
                }

                override fun onFailure(call: Call<ProductListResponseBody>, t: Throwable) {
                    Log.d("Product List 불러오기", "실패(서버 에러)")
                }
            })
    }

    fun getTopProductList(category: Long, binding: FragmentMainBinding, fragment: Main){
        service.getTopProductList(token = App.prefs.getString("access_token", ""), category).enqueue(object : Callback<ProductListResponseBody>{
            override fun onResponse(
                call: Call<ProductListResponseBody>,
                response: Response<ProductListResponseBody>,
            ) {
                if(response.isSuccessful){
                    val topItemList = response.body()!!.message.productList
                    val topItemAdapter = TopItemAdapter(topItemList as ArrayList<ProductList>, binding.root.context)

                    binding.apply {
                        topItemRv.adapter = topItemAdapter
                        topItemAdapter.setOnItemClickListener(object :
                            TopItemAdapter.onItemClickListener {
                            override fun onItemClick(position: Int) {
                                var intent =
                                    Intent(binding.root.context, DetailActivity::class.java)
                                var item = topItemAdapter.getItem(position)

                                intent.putExtra("productId", item.id)
                                intent.putExtra("productName", item.productName)
                                intent.putExtra("productPath", item.images[0])
                                /*
                            val graphWeekFragment = graphWeek()
                            var bundle = Bundle()
                            bundle.putLong("productId", item.id)
                            val id = item.id
                            Log.e("보내는 아이디","$id")
                            graphWeekFragment.arguments = bundle
                            */

                                fragment.startActivity(intent)
                            }
                        })
                    }
                } else{

                }
            }

            override fun onFailure(call: Call<ProductListResponseBody>, t: Throwable) {

            }

        })
    }

    fun getProductDetails(id : Long, binding: ActivityDetailBinding, activity: DetailActivity) {
        service.getProductDetails(token = App.prefs.getString("access_token", ""), id).enqueue(object : Callback<ProductDetailsResponseBody>{
            @RequiresApi(Build.VERSION_CODES.N)
            override fun onResponse(
                call: Call<ProductDetailsResponseBody>,
                response: Response<ProductDetailsResponseBody>,
            ) {
                if(response.isSuccessful) {
                    var details = response.body()!!.message.productDetails
                    var recommend = response.body()!!.message.recommendProducts
                    val detailAdapter = ProductDetailsAdapter(details as ArrayList<ProductDetails>)
                    val recommendAdapter = RecommendProductAdapter(recommend as ArrayList<ProductList>, binding.root.context)


                    binding.apply {
                        binding.productDetailRecyclerView.layoutManager = LinearLayoutManager(this.root.context, LinearLayoutManager.VERTICAL, false)
                        binding.productDetailRecyclerView.adapter = detailAdapter
                        
                        recommendListRecyclerView.layoutManager = LinearLayoutManager(this.root.context, LinearLayoutManager.HORIZONTAL, false)
                        recommendListRecyclerView.adapter = recommendAdapter
                        recommendAdapter.setOnItemClickListener(object: RecommendProductAdapter.onItemClickListener{
                            override fun onItemClick(position: Int) {
                                var intent =
                                    Intent(binding.root.context, DetailActivity::class.java)
                                var item = recommendAdapter.getItem(position)

                                intent.putExtra("productId", item.id)
                                intent.putExtra("productName", item.productName)
                                intent.putExtra("productPath", item.images[0])

                                activity.startActivity(intent)
                            }
                        })
                    }

                } else{
                    val retrofitRefresh = RetrofitRefresh()
                    retrofitRefresh.refreshToken()
                    getProductDetails(id, binding, activity)
                }
            }

            override fun onFailure(call: Call<ProductDetailsResponseBody>, t: Throwable) {
                Log.d("Product Details 불러오기", "실패(서버 에러)")
            }

        })
    }
}