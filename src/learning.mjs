// The atlas links to existing notes; a note can also live outside the atlas.
export function articlesForTopic(items,topic){
 return items.filter(item=>['notes','learn'].includes(item.type)&&item.topic===topic&&(!item.status||item.status==='published'));
}
export const articlePath=item=>`/${item.lang}/${item.type}/${item.slug}/`;
