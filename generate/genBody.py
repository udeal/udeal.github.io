from csv import reader

str1='<div class="card_deal"><table width="100%" cellpadding="4" cellspacing="0"><tbody><tr height="125"><td width="125" align="center" valign="center"><a href="'
str2='" target="_blank"><img src="'
str3='" style="max-width: 100px; max-height: 100px"></a></td><td width="15"></td><td><h4><a href="'
str4='" target="_blank">'
str5='</a></h4>                              <p><span style="font-size:20px;">Price: &nbsp;'
str6='</span><span style="font-size:12px;">&nbsp;&nbsp;&nbsp;(as of '
str7=')</span> </p>   <ul class="list-inline">    <li class="mr-none" title="" data-toggle="tooltip" data-original-title="Source"> <a rel="nofollow noopener" href="www.amazon.com" target="_blank">  <span style="font-size:10px;">From Amazon.com</span> </a> </li>  </ul>  </td>  <td width="10"></td> </tr> </tbody>  </table> </div>'

text=''
url_list=[]
with open("amz.csv", "r") as infile, open("body.html", "w") as outfile:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(infile)
    next(csv_reader, None)  # skip the headers

    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        # only show those has discount
        if (float(row[3]) != 0):
            url = row[4] + '?tag=udeals0d-20&linkCode=ogi&th=1'
            if url not in url_list:
                url_list.append(url)
                #print (url_list.index(url))
                price = '<span style="color:red;">' + row[2] + "</span>  (was $<strike>" + row[3] + "</strike>)"
                text = str1 + url + str2 + row[5] + str3 + url + str4 + row[1] + str5 + price + str6 + row[7] + str7
                outfile.write(text)
infile.close()
outfile.close()
